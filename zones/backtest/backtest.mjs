// Backtest historico de las zonas de Mi Mesa.
//
// Corre el MISMO motor del indicador de TradingView (tdl-indicators/mi_mesa_zonas.pine: niveles, FVG, perfil,
// marcos D/4H/1H, agrupado, calificacion, stop/TP, estados y gatillo de 5 min) sobre las velas de 5 min que el
// bus ya guarda (bars/<dia>.json, Yahoo, desde agosto 2026) y escribe los eventos con el mismo formato que manda
// el indicador por webhook. Asi el agente arranca con cientos de zonas resueltas en vez de esperar semanas.
//
//   node zones/backtest/backtest.mjs            -> zones/backtest/events.jsonl + zones/backtest/summary.json
//   node zones/backtest/backtest.mjs NQ ETHUSDT -> solo esos simbolos
//
// Diferencias con el vivo (por eso el analisis los reporta aparte, como "historico"):
//  - Yahoo no trae volumen en el bus: el VWAP y el perfil (VAH/VAL/POC) se calculan con peso igual por vela
//    (TWAP y perfil de tiempo). Es una aproximacion.
//  - No hay regimen de Market Regime (reg vacio) ni VIX. El sesgo del plan sale de plans/ (el plan del Session
//    Analyst vigente a esa hora, hasta 18 h), como haria la linea de sync.
//  - Se simula un grafico de 5 min con velas cerradas (sin ticks dentro de la vela).
// Si cambias el motor en el .pine, cambia tambien este archivo.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const BUS = path.resolve(HERE, '..', '..');
const VER = '3.5';
const SYMS = ['NQ', 'ES', 'GC', 'ETHUSDT', 'BTCUSDT'];
const TICK = { NQ: 0.25, ES: 0.25, GC: 0.1, ETHUSDT: 0.01, BTCUSDT: 0.01 };
const CRYPTO = new Set(['ETHUSDT', 'BTCUSDT']);

// mismos valores por defecto que los inputs del indicador
const P = { profRows: 50, vaPct: 0.7, fvgMax: 3, fvgMinPct: 2.0, ibMin: 60, trgWin: 30 };
// pesos v1 (DEFAULT_WEIGHTS de _intraday.mjs); el agente puede pasar otros con BACKTEST_WEIGHTS=<json>
const W = {
  decay: 0.7, align: 1.5, chop: 0.5, reg: 0.5, far: 1, farAtr: 12, lowrr: 1, rrMin: 1.2, ap: 7, a: 5, b: 3.5,
  ...(process.env.BACKTEST_WEIGHTS ? JSON.parse(process.env.BACKTEST_WEIGHTS) : {})
};
const wk = (k, d) => (W[k] !== undefined ? W[k] : d);

// ------------------------------------------------------------------ datos
function loadBars(sym) {
  const m = new Map();
  for (const f of fs.readdirSync(path.join(BUS, 'bars')).filter((x) => x.endsWith('.json')).sort()) {
    let d;
    try { d = JSON.parse(fs.readFileSync(path.join(BUS, 'bars', f), 'utf8')); } catch (e) { continue; }
    for (const b of d.symbols?.[sym] || []) m.set(b[0], b);
  }
  return [...m.values()].sort((a, b) => a[0] - b[0]).filter((b) => b[0] % 300 === 0)
    .map(([t, o, h, l, c]) => ({ t: t * 1000, o, h, l, c }));
}

function loadPlans() {
  const out = { fut: [], crypto: [] };
  const rd = (p) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { return null; } };
  for (const f of fs.readdirSync(path.join(BUS, 'plans')).filter((x) => /^\d{4}-\d{2}-\d{2}.*\.json$/.test(x))) {
    const d = rd(path.join(BUS, 'plans', f));
    const at = Date.parse(d?.generatedAt || d?.builtAt || '');
    if (d && Number.isFinite(at)) out.fut.push({ at, ins: d.instruments || {} });
  }
  const cdir = path.join(BUS, 'plans', 'crypto');
  if (fs.existsSync(cdir)) for (const f of fs.readdirSync(cdir).filter((x) => x.endsWith('.json'))) {
    const d = rd(path.join(cdir, f));
    const at = Date.parse(d?.builtAt || d?.generatedAt || '');
    if (d && Number.isFinite(at)) out.crypto.push({ at, ins: d.instruments || {} });
  }
  out.fut.sort((a, b) => a.at - b.at); out.crypto.sort((a, b) => a.at - b.at);
  return out;
}

function planAt(list, sym, t) {
  let best = null;
  for (const p of list) { if (p.at <= t) best = p; else break; }
  if (!best || t - best.at > 18 * 3600e3) return { bias: '', conv: '' };
  const i = best.ins[sym] || best.ins[sym.replace('USDT', '')];
  if (!i) return { bias: '', conv: '' };
  return { bias: String(i.biasSession || i.biasDay || '').toUpperCase(), conv: String(i.conviction || '').toLowerCase() };
}

// ------------------------------------------------------------------ tiempo (Chicago / NY)
const fmtCT = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Chicago', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', weekday: 'short', hourCycle: 'h23' });
const fmtNY = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', day: '2-digit' });
function ctParts(ms) {
  const p = Object.fromEntries(fmtCT.formatToParts(new Date(ms)).map((x) => [x.type, x.value]));
  return { date: `${p.year}-${p.month}-${p.day}`, y: +p.year, mo: +p.month, d: +p.day, hh: +p.hour, mm: +p.minute, wd: p.weekday };
}
const addDay = (date, n) => new Date(Date.parse(date + 'T12:00:00Z') + n * 86400e3).toISOString().slice(0, 10);
const mondayOf = (date) => { const d = new Date(date + 'T12:00:00Z'); const k = (d.getUTCDay() + 6) % 7; return addDay(date, -k); };

// ------------------------------------------------------------------ indicadores de apoyo
class RMA { constructor(n) { this.n = n; this.v = null; this.buf = []; } push(x) { if (this.v === null) { this.buf.push(x); if (this.buf.length === this.n) this.v = this.buf.reduce((a, b) => a + b, 0) / this.n; } else this.v = (this.v * (this.n - 1) + x) / this.n; return this.v; } }
class EMA { constructor(n) { this.k = 2 / (n + 1); this.n = n; this.v = null; this.buf = []; } push(x) { if (this.v === null) { this.buf.push(x); if (this.buf.length === this.n) this.v = this.buf.reduce((a, b) => a + b, 0) / this.n; } else this.v = x * this.k + this.v * (1 - this.k); return this.v; } }
// pivote confirmado: la vela de hace R es mayor (menor) que las L de la izquierda y las R de la derecha
class Pivots {
  constructor(L, R) { this.L = L; this.R = R; this.h = []; this.l = []; this.ph = null; this.pl = null; }
  push(hi, lo) {
    this.h.push(hi); this.l.push(lo);
    const n = this.L + this.R + 1;
    if (this.h.length > n) { this.h.shift(); this.l.shift(); }
    let newH = null, newL = null;
    if (this.h.length === n) {
      const c = this.L, ch = this.h[c], cl = this.l[c];
      let okH = true, okL = true;
      for (let i = 0; i < n; i++) {
        if (i === c) continue;
        if (i < c ? this.h[i] >= ch : this.h[i] > ch) okH = false;
        if (i < c ? this.l[i] <= cl : this.l[i] < cl) okL = false;
      }
      if (okH) { this.ph = ch; newH = ch; }
      if (okL) { this.pl = cl; newL = cl; }
    }
    return { newH, newL };
  }
}
// flecha del Trend Checklist (f_arrow) en una temporalidad: se alimenta con velas cerradas
class Arrow {
  constructor() { this.e20 = new EMA(20); this.piv = new Pivots(3, 3); this.h1 = null; this.h2 = null; this.l1 = null; this.l2 = null; this.bos = 0; this.arrow = 0; }
  push(b) {
    const e = this.e20.push(b.c);
    const { newH, newL } = this.piv.push(b.h, b.l);
    if (newH !== null) { this.h2 = this.h1; this.h1 = newH; }
    if (newL !== null) { this.l2 = this.l1; this.l1 = newL; }
    if (this.h1 !== null && b.c > this.h1) this.bos = 1;
    if (this.l1 !== null && b.c < this.l1) this.bos = -1;
    const ok = this.h1 !== null && this.h2 !== null && this.l1 !== null && this.l2 !== null;
    const seq = ok && this.h1 > this.h2 && this.l1 > this.l2 ? 1 : ok && this.h1 < this.h2 && this.l1 < this.l2 ? -1 : 0;
    const st = this.bos === 0 || this.bos === seq ? seq : seq === 0 ? this.bos * 2 : this.bos * 3;
    this.arrow = e !== null && st > 0 && b.c > e ? 1 : e !== null && st < 0 && b.c < e ? -1 : 0;
    return this.arrow;
  }
}
// agregador de velas de temporalidad mayor: devuelve la vela que se cerro cuando cambia la clave
class Agg {
  constructor() { this.key = null; this.cur = null; }
  push(key, b) {
    let closed = null;
    if (this.key !== key) { closed = this.cur; this.key = key; this.cur = { t: b.t, o: b.o, h: b.h, l: b.l, c: b.c }; }
    else { this.cur.h = Math.max(this.cur.h, b.h); this.cur.l = Math.min(this.cur.l, b.l); this.cur.c = b.c; }
    return closed;
  }
}

// ------------------------------------------------------------------ FVG (igual que el indicador)
function fvgAdd(gs, d, bLo, bHi, sLo, sHi, dATR) {
  const minSz = (dATR || 0) * P.fvgMinPct / 100;
  if (d === 1 && bHi - bLo >= minSz) gs.push({ lo: bLo, hi: bHi, dir: 1, inv: false });
  if (d === -1 && sHi - sLo >= minSz) gs.push({ lo: sLo, hi: sHi, dir: -1, inv: false });
  if (gs.length > 24) gs.shift();
}
function fvgUpdate(gs, b) {
  for (let i = gs.length - 1; i >= 0; i--) {
    const g = gs[i];
    let drop = false;
    if (!g.inv) {
      if (g.dir === 1 && b.l < g.hi && b.l > g.lo) g.hi = b.l;
      else if (g.dir === -1 && b.h > g.lo && b.h < g.hi) g.lo = b.h;
    }
    if (!g.inv) {
      if (g.dir === 1 && b.c < g.lo) { g.inv = true; g.dir = -1; }
      else if (g.dir === -1 && b.c > g.hi) { g.inv = true; g.dir = 1; }
    } else drop = (g.dir === -1 && b.c > g.hi) || (g.dir === 1 && b.c < g.lo);
    if (drop) gs.splice(i, 1);
  }
}
// FVG de una temporalidad mayor con sus 3 ultimas velas cerradas (low[1] > high[3] ...)
function htfGap(hist, gs, dATR) {
  if (hist.length < 3) return;
  const b1 = hist[hist.length - 1], b3 = hist[hist.length - 3];
  const d = b1.l > b3.h ? 1 : b1.h < b3.l ? -1 : 0;
  fvgAdd(gs, d, b3.h, b1.l, b1.h, b3.l, dATR);
}

// ------------------------------------------------------------------ motor (f_plan + f_grade)
const rt = (x, tick) => Math.round(x / tick) * tick;
function grade(mem, side, distAtr, rr1, ctx) {
  const ws = mem.map((m) => m.w * m.f).sort((a, b) => b - a);
  let score = 0;
  ws.forEach((w, i) => { score += w * Math.pow(wk('decay', 0.7), i); });
  if (ctx.fvDir === side) score += wk('align', 1.5); else if (ctx.fvDir === -side) score -= wk('align', 1.5);
  if (ctx.regime === 'CHOP') score -= wk('chop', 0.5);
  if ((ctx.regime === 'BULL' && side === 1) || (ctx.regime === 'BEAR' && side === -1)) score += wk('reg', 0.5);
  if (distAtr > wk('farAtr', 12)) score -= wk('far', 1);
  if (rr1 !== null && rr1 < wk('rrMin', 1.2)) score -= wk('lowrr', 1);
  const aligned = ctx.fvDir === side;
  let g = score >= wk('ap', 7) && aligned ? 'A+' : score >= wk('a', 5) ? 'A' : score >= wk('b', 3.5) ? 'B' : 'C';
  if (!aligned && g === 'A+') g = 'A';
  if (ctx.fvDir === -side && g === 'A') g = 'B';
  return { score, grade: g };
}

function plan(price, L, gaps, ctx, tick) {
  const out = [];
  const { atr5, dATR } = L;
  if (price == null || !(atr5 > 0) || !(dATR > 0)) return out;
  const tol = Math.max(atr5 * 0.5, tick * 4), maxW = atr5 * 2.2, reach = dATR * 0.9;
  const els = [];
  const lv = (px, k, w, nm) => { if (px != null && Number.isFinite(px)) els.push({ lo: px, hi: px, w: wk(k, w), nm, k, f: 1 }); };
  lv(L.pdh, 'pdh', 2.5, 'Max ayer'); lv(L.pdl, 'pdl', 2.5, 'Min ayer');
  lv(L.pwh, 'pwh', 2.5, 'Max semana'); lv(L.pwl, 'pwl', 2.5, 'Min semana');
  lv(L.pmh, 'pmh', 2.0, 'Max mes'); lv(L.pml, 'pml', 2.0, 'Min mes');
  lv(L.onH, 'onh', 2.0, 'ONH'); lv(L.onL, 'onl', 2.0, 'ONL');
  lv(L.asH, 'asH', 1.5, 'Max Asia'); lv(L.asL, 'asL', 1.5, 'Min Asia');
  lv(L.loH, 'loH', 1.5, 'Max Londres'); lv(L.loL, 'loL', 1.5, 'Min Londres');
  lv(L.ibH, 'ibh', 1.5, 'IBH'); lv(L.ibL, 'ibl', 1.5, 'IBL');
  lv(L.pVah, 'vah', 2.0, 'VAH'); lv(L.pVal, 'val', 2.0, 'VAL'); lv(L.pPoc, 'poc', 2.0, 'POC');
  lv(L.dVah, 'dvah', 1.5, 'VAH hoy'); lv(L.dVal, 'dval', 1.5, 'VAL hoy'); lv(L.dPoc, 'dpoc', 1.5, 'POC hoy');
  lv(L.pdc, 'pdc', 1.0, 'Cierre ayer');
  lv(L.pdh != null && L.pdl != null ? (L.pdh + L.pdl) / 2 : null, 'pdMid', 1.0, 'Mitad ayer');
  lv(L.dOpen, 'do', 1.5, 'Apertura dia'); lv(L.tdo, 'tdo', 1.5, 'TDO');
  lv(L.wOpen, 'wo', 1.5, 'Apertura semana'); lv(L.mOpen, 'mOpen', 1.0, 'Apertura mes');
  lv(L.sh1h, 'sh1h', 2.0, 'Max 1h'); lv(L.sl1h, 'sl1h', 2.0, 'Min 1h');
  lv(L.sh4h, 'sh4h', 2.5, 'Max 4h'); lv(L.sl4h, 'sl4h', 2.5, 'Min 4h');
  lv(L.sh5, 'sh5', 0.5, 'Max 5m'); lv(L.sl5, 'sl5', 0.5, 'Min 5m');
  lv(L.ema200, 'ema200', 1.0, 'EMA200 5m'); lv(L.e50h, 'ema50h', 1.0, 'EMA50 1h');
  lv(L.vwapUp, 'vwapUp', 1.0, 'VWAP banda alta'); lv(L.vwapDn, 'vwapDn', 1.0, 'VWAP banda baja'); lv(L.vwap, 'vwap', 1.0, 'VWAP');
  for (const [gs, tfl, w] of [[gaps.g5, '5m', 1.0], [gaps.g15, '15m', 1.5], [gaps.g60, '1h', 2.5], [gaps.g240, '4h', 3.0]]) {
    const idx = gs.map((g, i) => [Math.abs(price - (g.lo + g.hi) / 2), i]).sort((a, b) => a[0] - b[0]).slice(0, P.fvgMax);
    for (const [, i] of idx) {
      const g = gs[i];
      const lbl = (g.inv ? 'i' : '') + 'FVG ' + tfl + (g.dir === 1 ? ' ▲' : ' ▼');
      const k = 'f' + tfl, ww = wk(k, w);
      if (g.hi - g.lo > maxW) {
        const nearE = Math.abs(g.hi - price) < Math.abs(g.lo - price) ? g.hi : g.lo;
        els.push({ lo: nearE, hi: nearE, w: ww, nm: lbl + ' borde', k, f: 1 });
        const ce = (g.lo + g.hi) / 2;
        els.push({ lo: ce, hi: ce, w: ww, nm: lbl + ' mitad', k, f: 0.6 });
      } else els.push({ lo: g.lo, hi: g.hi, w: ww, nm: lbl, k, f: 1 });
    }
  }
  const rngHi = Math.max(L.pdh ?? L.hod, L.hod), rngLo = Math.min(L.pdl ?? L.lod, L.lod), rngW = rngHi - rngLo;
  if (rngW > 0) {
    const gl1 = rngLo + rngW * 0.214, gl2 = rngLo + rngW * 0.382, gs1 = rngLo + rngW * 0.618, gs2 = rngLo + rngW * 0.786;
    if (Math.abs(gl2 - gl1) <= maxW * 1.5) els.push({ lo: gl1, hi: gl2, w: wk('gz', 1.5), nm: 'Zona de descuento', k: 'gz', f: 1 });
    if (Math.abs(gs2 - gs1) <= maxW * 1.5) els.push({ lo: gs1, hi: gs2, w: wk('gz', 1.5), nm: 'Zona cara', k: 'gz', f: 1 });
  }
  const near = els.filter((e) => Math.abs((e.lo + e.hi) / 2 - price) <= reach).sort((a, b) => a.lo - b.lo);
  const cl = [];
  for (const e of near) {
    const c = cl[cl.length - 1];
    if (c && e.lo <= c.hi + tol && Math.max(c.hi, e.hi) - c.lo <= maxW) { c.hi = Math.max(c.hi, e.hi); c.m.push(e); }
    else cl.push({ lo: e.lo, hi: e.hi, m: [e] });
  }
  const mids = cl.map((c) => (c.lo + c.hi) / 2);
  const zs = [];
  for (const c of cl) {
    let lo = c.lo, hi = c.hi;
    if (hi - lo < atr5 * 0.4) { const m0 = (lo + hi) / 2; lo = m0 - atr5 * 0.2; hi = m0 + atr5 * 0.2; }
    const mid = (lo + hi) / 2;
    const inside = price >= lo && price <= hi;
    const side = inside ? (ctx.fvDir >= 0 ? 1 : -1) : mid < price ? 1 : -1;
    const distPts = inside ? 0 : side === 1 ? price - hi : lo - price;
    const distAtr = distPts / atr5;
    const buf = Math.max(atr5 * 0.3, tick * 4);
    const entry = rt(side === 1 ? hi - (hi - lo) * 0.25 : lo + (hi - lo) * 0.25, tick);
    let stopRaw = side === 1 ? lo - buf : hi + buf;
    if (Math.abs(entry - stopRaw) < atr5 * 0.75) stopRaw = entry - side * atr5 * 0.75;
    const stop = rt(stopRaw, tick), risk = Math.abs(entry - stop);
    const ahead = mids.filter((mm) => (side === 1 ? mm > entry + risk * 0.8 : mm < entry - risk * 0.8)).sort((a, b) => a - b);
    if (side === -1) ahead.reverse();
    const cap = entry + side * risk * 3;
    const lvl1 = ahead.length ? ahead[0] : null;
    const tp1 = rt(lvl1 !== null && (side === 1 ? lvl1 < cap : lvl1 > cap) ? lvl1 : cap, tick);
    const nxt = ahead.find((mm) => (side === 1 ? mm > tp1 + risk * 0.5 : mm < tp1 - risk * 0.5));
    const tp2 = rt(nxt !== undefined ? nxt : tp1 + side * risk * 2, tick);
    const rr1 = risk > 0 ? Math.round(Math.abs(tp1 - entry) / risk * 100) / 100 : null;
    const { score, grade: g } = grade(c.m, side, distAtr, rr1, ctx);
    const sorted = c.m.slice().sort((a, b) => b.w * b.f - a.w * a.f);
    const names = [], keys = [];
    for (const m of sorted) { if (!names.includes(m.nm)) names.push(m.nm); if (!keys.includes(m.k)) keys.push(m.k); }
    const id = (side === 1 ? 'long:' : 'short:') + (Math.round(mid / (tick * 4)) * tick * 4).toFixed(2);
    zs.push({ id, side, lo: rt(lo, tick), hi: rt(hi, tick), mid: rt(mid, tick), entry, stop, tp1, tp2, rr1, distAtr, inside, score, grade: g, aligned: ctx.fvDir === side, conf: names.join(' · '), keys: keys.join('+') });
  }
  const us = zs.filter((z) => z.grade !== 'C').sort((a, b) => b.score - a.score);
  let nL = 0, nS = 0;
  for (const z of us) { if (z.side === 1 && nL < 3) { out.push(z); nL++; } else if (z.side === -1 && nS < 3) { out.push(z); nS++; } }
  return out;
}

// ------------------------------------------------------------------ simulacion de un simbolo
function run(sym, bars, plans) {
  const tick = TICK[sym];
  const crypto = CRYPTO.has(sym);
  const events = [];
  // series de 5 min
  const tr5 = new RMA(14), ema200 = new EMA(200), piv5 = new Pivots(3, 3);
  const trWin = [], hiWin = [], loWin = [];
  // temporalidades mayores
  const aggD = new Agg(), aggW = new Agg(), aggM = new Agg(), agg60 = new Agg(), agg240 = new Agg(), agg15 = new Agg();
  const atrD = new RMA(14);
  let dATR = null, prevD = null, prevW = null, prevM = null, dOpen = null, wOpen = null, mOpen = null, lastDc = null;
  const e50 = new EMA(50), piv1h = new Pivots(5, 5), piv4h = new Pivots(3, 3);
  let e50h = null, sh1h = null, sl1h = null, sh4h = null, sl4h = null;
  const arrD = new Arrow(), arr4 = new Arrow(), arr1 = new Arrow();
  let tcD = 0, tc4 = 0, tc1 = 0;
  const h15 = [], h60 = [], h240 = [];
  const gaps = { g5: [], g15: [], g60: [], g240: [] };
  const last5 = [];
  // sesiones
  const sess = { as: { in: false, h: null, l: null }, lo: { in: false, h: null, l: null }, on: { in: false, h: null, l: null } };
  let inRTHp = false, ibH = null, ibL = null, ibEnd = null, tdo = null, nyDay = null;
  let hod = null, lod = null;
  // vwap / perfil (peso igual por vela: el bus no tiene volumen)
  let vN = 0, vS = 0, vS2 = 0;
  let prof = new Map(), profRs = null, dPoc = null, dVah = null, dVal = null, pPoc = null, pVah = null, pVal = null;
  // estado de zonas
  let st = new Map();
  let chiDay = null;
  let first = true;

  for (let i = 0; i < bars.length; i++) {
    const b = bars[i];
    const ct = ctParts(b.t);
    const m = ct.hh * 60 + ct.mm;
    // dia de trading: futuros abren a las 17:00 CT (cuenta para el dia siguiente); cripto, dia UTC
    const tday = crypto ? new Date(b.t).toISOString().slice(0, 10) : (ct.hh >= 17 ? addDay(ct.date, 1) : ct.date);
    const wkey = mondayOf(tday), mkey = tday.slice(0, 7);
    const newDay = !first && tday !== aggD.key;

    // --- velas D / W / M cerradas
    const cD = aggD.push(tday, b);
    if (cD) {
      const tr = lastDc === null ? cD.h - cD.l : Math.max(cD.h - cD.l, Math.abs(cD.h - lastDc), Math.abs(cD.l - lastDc));
      dATR = atrD.push(tr); lastDc = cD.c; prevD = cD;
      tcD = arrD.push(cD);
    }
    if (aggD.cur.t === b.t) dOpen = b.o;
    const cW = aggW.push(wkey, b); if (cW) prevW = cW; if (aggW.cur.t === b.t) wOpen = b.o;
    const cM = aggM.push(mkey, b); if (cM) prevM = cM; if (aggM.cur.t === b.t) mOpen = b.o;
    // --- 15m / 1h / 4h (4h de CME alineado a las 17:00 CT; cripto a UTC)
    const k15 = Math.floor(b.t / 900e3), k60 = Math.floor(b.t / 3600e3);
    const k240 = crypto ? Math.floor(b.t / 14400e3) : tday + ':' + Math.floor(((ct.hh - 17 + 24) % 24) / 4);
    const c15 = agg15.push(k15, b); if (c15) { h15.push(c15); if (h15.length > 5) h15.shift(); htfGap(h15, gaps.g15, dATR); }
    const c60 = agg60.push(k60, b);
    if (c60) {
      h60.push(c60); if (h60.length > 5) h60.shift(); htfGap(h60, gaps.g60, dATR);
      e50h = e50.push(c60.c); piv1h.push(c60.h, c60.l); sh1h = piv1h.ph; sl1h = piv1h.pl; tc1 = arr1.push(c60);
    }
    const c240 = agg240.push(k240, b);
    if (c240) {
      h240.push(c240); if (h240.length > 5) h240.shift(); htfGap(h240, gaps.g240, dATR);
      piv4h.push(c240.h, c240.l); sh4h = piv4h.ph; sl4h = piv4h.pl; tc4 = arr4.push(c240);
    }
    // --- 5m (grafico)
    const prevC = i > 0 ? bars[i - 1].c : null;
    const tr = prevC === null ? b.h - b.l : Math.max(b.h - b.l, Math.abs(b.h - prevC), Math.abs(b.l - prevC));
    const atr5 = tr5.push(tr);
    const e200 = ema200.push(b.c);
    trWin.push(tr); hiWin.push(b.h); loWin.push(b.l);
    if (trWin.length > 14) { trWin.shift(); hiWin.shift(); loWin.shift(); }
    const chopIdx = trWin.length === 14 ? 100 * Math.log10(trWin.reduce((a, x) => a + x, 0) / (Math.max(...hiWin) - Math.min(...loWin))) / Math.log10(14) : null;
    piv5.push(b.h, b.l);
    last5.push(b); if (last5.length > 3) last5.shift();
    if (last5.length === 3) {
      const b0 = last5[2], b2 = last5[0];
      fvgAdd(gaps.g5, b0.l > b2.h ? 1 : b0.h < b2.l ? -1 : 0, b2.h, b0.l, b0.h, b2.l, dATR);
    }
    for (const gs of Object.values(gaps)) fvgUpdate(gs, b);
    // --- sesiones (Chicago)
    const ny = fmtNY.format(new Date(b.t));
    if (nyDay !== null && ny !== nyDay) tdo = b.o;
    nyDay = ny;
    const inS = { as: m >= 1020 || m < 120, lo: m >= 120 && m < 510, on: m >= 1020 || m < 510 };
    for (const k of ['as', 'lo', 'on']) {
      const s = sess[k];
      if (inS[k] && !s.in) { s.h = b.h; s.l = b.l; } else if (inS[k]) { s.h = Math.max(s.h, b.h); s.l = Math.min(s.l, b.l); }
      s.in = inS[k];
    }
    const inRTH = m >= 510 && m < 900;
    if (inRTH && !inRTHp) { ibH = b.h; ibL = b.l; ibEnd = b.t + P.ibMin * 60e3; }
    else if (inRTH && ibEnd !== null && b.t < ibEnd) { ibH = Math.max(ibH, b.h); ibL = Math.min(ibL, b.l); }
    inRTHp = inRTH;
    if (newDay || hod === null) { hod = b.h; lod = b.l; } else { hod = Math.max(hod, b.h); lod = Math.min(lod, b.l); }
    // vwap
    if (newDay || first) { vN = 0; vS = 0; vS2 = 0; }
    const src = (b.h + b.l + b.c) / 3;
    vN += 1; vS += src; vS2 += src * src;
    const vwap = vS / vN, sd = Math.sqrt(Math.max(0, vS2 / vN - vwap * vwap));
    // perfil del dia
    const rsNow = dATR > 0 ? dATR / P.profRows : 20 * tick;
    if (newDay) { pPoc = dPoc; pVah = dVah; pVal = dVal; prof = new Map(); profRs = Math.max(rsNow, tick); }
    if (profRs === null) profRs = Math.max(rsNow, tick);
    {
      const lb = Math.floor(b.l / profRs), hb = Math.floor(b.h / profRs);
      const vper = 1 / Math.max(1, hb - lb + 1);
      for (let k = lb; k <= hb; k++) prof.set(k, (prof.get(k) || 0) + vper);
      const keys = [...prof.keys()];
      let tot = 0, pocKey = 0, pocVol = -1;
      for (const k of keys) { const v = prof.get(k); tot += v; if (v > pocVol) { pocVol = v; pocKey = k; } }
      keys.sort((a, c) => a - c);
      const pi = keys.indexOf(pocKey);
      let lo_i = pi, hi_i = pi, acc = pocVol;
      while (acc < tot * P.vaPct && (lo_i > 0 || hi_i < keys.length - 1)) {
        const up = hi_i < keys.length - 1 ? prof.get(keys[hi_i + 1]) : -1;
        const dn = lo_i > 0 ? prof.get(keys[lo_i - 1]) : -1;
        if (up >= dn) { hi_i++; acc += up; } else { lo_i--; acc += dn; }
      }
      dPoc = (pocKey + 0.5) * profRs; dVah = (keys[hi_i] + 1) * profRs; dVal = keys[lo_i] * profRs;
    }
    first = false;

    // --- plan y direccion
    const pl = planAt(crypto ? plans.crypto : plans.fut, sym, b.t);
    const saD = pl.bias === 'LONG' ? 1 : pl.bias === 'SHORT' ? -1 : 0;
    const saW = pl.conv === 'alta' ? 1.5 : 1;
    const fvScore = tcD + tc4 + tc1 * 0.5 + saD * saW;
    const fvDir = fvScore >= 1.5 ? 1 : fvScore <= -1.5 ? -1 : 0;
    const ctx = { fvDir, regime: '' };
    const L = {
      atr5, dATR, pdh: prevD?.h ?? null, pdl: prevD?.l ?? null, pdc: prevD?.c ?? null, dOpen, pwh: prevW?.h ?? null, pwl: prevW?.l ?? null, wOpen,
      pmh: prevM?.h ?? null, pml: prevM?.l ?? null, mOpen, onH: sess.on.h, onL: sess.on.l, asH: sess.as.h, asL: sess.as.l, loH: sess.lo.h, loL: sess.lo.l,
      ibH, ibL, pVah, pVal, pPoc, dVah, dVal, dPoc, tdo, sh1h, sl1h, sh4h, sl4h, sh5: piv5.ph, sl5: piv5.pl, ema200: e200, e50h,
      vwap, vwapUp: vwap + sd, vwapDn: vwap - sd, hod, lod
    };
    // calentamiento: hace falta el ATR diario y el de 5 min
    if (!(dATR > 0) || !(atr5 > 0)) continue;

    // --- estados (port de trackZones + gatillo); el registro se reinicia cada dia de Chicago
    if (chiDay !== null && ct.date !== chiDay) st = new Map();
    chiDay = ct.date;
    const sessNow = inRTH ? 'ny' : inS.lo ? 'london' : inS.as ? 'asia' : 'off';
    const stretchAtr = atr5 > 0 ? Math.abs(b.c - vwap) / atr5 : null;
    const zones = plan(b.c, L, gaps, ctx, tick);
    const feat = (z) => ({
      v: VER, src: 'backtest', score: +z.score.toFixed(2), rr: z.rr1, dist: +z.distAtr.toFixed(2), chop: chopIdx !== null ? +chopIdx.toFixed(2) : null,
      str: stretchAtr !== null ? +stretchAtr.toFixed(2) : null, keys: z.keys, tf: '5', risk: +Math.abs(z.entry - z.stop).toFixed(4),
      al: z.aligned ? '1' : fvDir === -z.side ? '-1' : '0', reg: '', sess: sessNow, wv: 'v1', bias: pl.bias || ''
    });
    const emit = (s, ev, extra = {}) => events.push({
      sym, ev, id: s.id, side: s.side === 1 ? 'long' : 'short', lo: s.lo, hi: s.hi, grade: s.grade, entry: s.entry, stop: s.stop, tp1: s.tp1,
      t: b.t, f: { ...s.feat, ...extra }
    });
    for (const s of st.values()) s.inPlan = false;
    for (const z of zones) {
      const s = st.get(z.id);
      if (s) {
        Object.assign(s, { lo: z.lo, hi: z.hi, entry: z.entry, stop: z.stop, tp1: z.tp1, grade: z.grade, conf: z.conf, inPlan: true });
        if (s.status === 'nueva' || s.status === 'activa' || s.status === 'tocada') s.feat = feat(z);
      } else {
        const ns = { id: z.id, side: z.side, lo: z.lo, hi: z.hi, entry: z.entry, stop: z.stop, tp1: z.tp1, grade: z.grade, created: b.t, status: z.inside ? 'tocada' : 'nueva', touched: z.inside ? b.t : null, inPlan: true, conf: z.conf, armed: null, feat: feat(z), mfeP: 0, maeP: 0 };
        st.set(z.id, ns);
        if (z.grade === 'A+' && !z.inside) emit(ns, 'nueva');
      }
    }
    for (const s of st.values()) {
      const before = s.status;
      if ((s.status === 'nueva' || s.status === 'activa') && b.t > s.created) {
        s.status = 'activa';
        const touched = s.side === 1 ? b.l <= s.hi : b.h >= s.lo;
        if (touched && s.inPlan) { s.status = 'tocada'; s.touched = b.t; }
      }
      // orden limite en la entrada de la zona (sin esperar gatillo): se llena si el precio la alcanza despues del toque
      // gatillo + retroceso: ya armada, una limite en la entrada se llena si el precio vuelve a ella (vela posterior)
      if (s.status === 'armada' && !s.pbFill && s.armed !== null && b.t > s.armed && (s.side === 1 ? b.l <= s.entry : b.h >= s.entry)) s.pbFill = true;
      if ((s.status === 'tocada' || s.status === 'armada') && !s.limFill && s.touched !== null && (s.side === 1 ? b.l <= s.entry : b.h >= s.entry)) s.limFill = true;
      if (s.status === 'armada') {
        s.mfeP = Math.max(s.mfeP, s.side === 1 ? b.h - s.entry : s.entry - b.l);
        s.maeP = Math.max(s.maeP, s.side === 1 ? s.entry - b.l : b.h - s.entry);
      }
      if (s.status === 'tocada' || s.status === 'armada') {
        if (s.side === 1 ? b.c < s.stop : b.c > s.stop) s.status = 'invalidada';
        else if (s.side === 1 ? b.c >= s.tp1 : b.c <= s.tp1) s.status = 'funciono';
      }
      if (s.status === 'tocada' && s.inPlan && s.touched !== null && b.t > s.touched && b.t - s.touched <= P.trgWin * 60e3) {
        const ok = s.side === 1 ? b.c > s.entry && b.c > b.o : b.c < s.entry && b.c < b.o;
        if (ok) { s.status = 'armada'; s.armed = b.t; s.fill = b.c; }
      }
      if (s.status !== before && ['tocada', 'armada', 'funciono', 'invalidada'].includes(s.status)) {
        const rk = Math.abs(s.entry - s.stop);
        const ex = (s.status === 'funciono' || s.status === 'invalidada') && rk > 0 ? { mfe: +(s.mfeP / rk).toFixed(2), mae: +(s.maeP / rk).toFixed(2) } : {};
        // R realista (solo historico): entras al cierre de la vela del gatillo; sales en TP1 o al cierre que invalida
        if (s.fill != null && (s.status === 'funciono' || s.status === 'invalidada')) {
          const rf = Math.abs(s.fill - s.stop);
          const exitPx = s.status === 'funciono' ? s.tp1 : b.c;
          if (rf > 0) ex.rx = +((s.side === 1 ? exitPx - s.fill : s.fill - exitPx) / rf).toFixed(2);
        }
        // R con orden limite en la entrada de la zona (rl; null = la limite nunca se lleno)
        if (s.status === 'funciono' || s.status === 'invalidada') {
          const exitPx = s.status === 'funciono' ? s.tp1 : b.c;
          ex.rl = s.limFill && rk > 0 ? +((s.side === 1 ? exitPx - s.entry : s.entry - exitPx) / rk).toFixed(2) : null;
          if (s.armed !== null) ex.rp = s.pbFill && rk > 0 ? +((s.side === 1 ? exitPx - s.entry : s.entry - exitPx) / rk).toFixed(2) : null;
        }
        emit(s, s.status, ex);
      }
    }
    for (const [k, s] of [...st]) if (!s.inPlan && (s.status === 'nueva' || s.status === 'activa')) st.delete(k);
  }
  return events;
}

// ------------------------------------------------------------------ main
const want = process.argv.slice(2).length ? process.argv.slice(2) : SYMS;
const plans = loadPlans();
const all = [];
const summary = { generatedAt: new Date().toISOString(), engine: 'mi_mesa_zonas.pine v' + VER, weights: W, notes: 'TWAP y perfil por tiempo (sin volumen), sin regimen ni VIX, grafico de 5 min con velas cerradas', symbols: {} };
for (const sym of want) {
  const bars = loadBars(sym);
  if (!bars.length) continue;
  const t0 = Date.now();
  const evs = run(sym, bars, plans);
  all.push(...evs);
  const cnt = (ev) => evs.filter((e) => e.ev === ev).length;
  summary.symbols[sym] = { bars: bars.length, from: new Date(bars[0].t).toISOString().slice(0, 10), to: new Date(bars[bars.length - 1].t).toISOString().slice(0, 10), tocada: cnt('tocada'), armada: cnt('armada'), funciono: cnt('funciono'), invalidada: cnt('invalidada'), secs: Math.round((Date.now() - t0) / 1000) };
  console.log(sym, JSON.stringify(summary.symbols[sym]));
}
all.sort((a, b) => a.t - b.t);
// solo zonas a las que el precio LLEGO (evento tocada o armada): las que nacieron con el precio adentro o nunca se
// tocaron no son un setup y solo pesan en el archivo
const dayCT = (ms) => ctParts(ms).date;
const keep = new Set(all.filter((e) => e.ev === 'tocada' || e.ev === 'armada').map((e) => e.sym + '|' + e.id + '|' + dayCT(e.t)));
const kept = all.filter((e) => keep.has(e.sym + '|' + e.id + '|' + dayCT(e.t)));
all.length = 0; all.push(...kept);
fs.writeFileSync(path.join(HERE, 'events.jsonl'), all.map((e) => JSON.stringify(e)).join('\n') + '\n');
fs.writeFileSync(path.join(HERE, 'summary.json'), JSON.stringify(summary, null, 1) + '\n');
console.log('eventos', all.length);
