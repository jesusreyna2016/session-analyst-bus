// Filtro de tendencia: no entrar en contra del movimiento.
// Usa velas de 5m de MFP (pedidas por el stream al cerrar cada vela) y calcula, por mercado:
//   ema20_50  EMA20 vs EMA50 de 5m     (short solo si EMA20 < EMA50)
//   ema200    precio vs EMA200 de 5m   (short solo si cierre < EMA200)
//   ema9_21   EMA9 vs EMA21 de 5m
//   struct5   estructura de 5m: ultimo evento (CHoCH/MSS, BOS, CISD, IFVG) a favor o neutro
//   struct15  lo mismo en 15m
//   cisd      direccion del ultimo CISD en 1m, 3m y 5m (CISD_TFS). Con CISD_MODE=last (por defecto) manda el CISD mas
//             reciente de cualquiera de ellas: un CISD alcista habilita longs y bloquea shorts hasta un CISD bajista.
//             Con CISD_MODE=all, el ultimo CISD de cada temporalidad tiene que coincidir. Usa velas de 1m pedidas cada minuto.
//   vwap      precio vs VWAP de la sesion (desde 17:00 CT). Como MFP no da volumen en los indices, es un TWAP
//             (promedio del precio tipico), igual que en el historico de las zonas.
// Una zona se opera solo si pasan TODOS los filtros activos (TREND_FILTERS). Si cambian en contra, la orden
// en espera se cancela (la zona deja de ser elegible).
import { toBars, analyze, allows } from './structure.mjs';

const FIVE = 300000;
const MIN = 60000;
// junta velas de 1m en velas de n minutos (solo las completas)
const aggMin = (b1, n) => {
  if (n === 1) return b1;
  const out = [];
  for (const b of b1) {
    const k = Math.floor(b.t / (n * MIN)) * n * MIN;
    const l = out[out.length - 1];
    if (l && l.t === k) { l.h = Math.max(l.h, b.h); l.l = Math.min(l.l, b.l); l.c = b.c; l.cnt++; } else out.push({ ...b, t: k, cnt: 1 });
  }
  return out.filter((x) => x.cnt === n);
};
const ema = (a, n) => { let e = null; const k = 2 / (n + 1); for (const x of a) e = e == null ? x : e + (x - e) * k; return e; };
const agg = (b5, n) => {
  const out = [];
  for (const b of b5) {
    const k = Math.floor(b.t / (n * FIVE)) * n * FIVE;
    const l = out[out.length - 1];
    if (l && l.t === k) { l.h = Math.max(l.h, b.h); l.l = Math.min(l.l, b.l); l.c = b.c; l.cnt++; } else out.push({ ...b, t: k, cnt: 1 });
  }
  return out.filter((x) => x.cnt === n);
};
const ctHour = (t) => +new Intl.DateTimeFormat('en-US', { timeZone: 'America/Chicago', hour: 'numeric', hourCycle: 'h23' }).format(new Date(t));
const sessionStart = (t) => { let s = Math.floor(t / 3600000) * 3600000; for (let i = 0; i < 30; i++) { if (ctHour(s) === 17) return s; s -= 3600000; } return t - 86400000; };

export const TREND_FILTERS = ['cisd', 'ema20_50', 'ema200', 'ema9_21', 'struct5', 'struct15', 'vwap'];

export class Trend {
  constructor(cfg, stream, log) {
    this.cfg = cfg;
    this.stream = stream;
    this.log = log;
    this.filters = cfg.trendFilters;
    this.state = new Map(); // sym -> {bar, at, ...}
    this.cisd = new Map(); // sym -> {cur, triedAt, lastBar, tfs: {1:{dir,t}, ...}, dir, at}
    this.needCisd = this.filters.includes('cisd');
    this.need5 = this.filters.some((f) => f !== 'cisd');
  }

  enabled() { return this.filters.length > 0; }

  // pide velas cuando cierra una nueva de 5m (con 8 s de margen para que MFP la tenga final)
  async refresh(meta) {
    if (!this.enabled()) return;
    if (this.needCisd) await this.refreshCisd(meta);
    if (!this.need5) return;
    const cur = Math.floor((Date.now() - 8000) / FIVE) * FIVE; // apertura de la vela en curso
    for (const [sym, m] of Object.entries(meta)) {
      const s = this.state.get(sym);
      if (s && s.cur === cur) continue;
      if (s && Date.now() - s.triedAt < 20000) continue;
      try {
        const r = await this.stream.request('candles.history', { provider: m.provider, symbol: m.coin, interval: '5m', startTime: Date.now() - 5 * 86400000, endTime: Date.now(), limit: 1000 });
        const bars = toBars(r).filter((b) => b.t < cur).slice(-600);
        if (bars.length < 220) throw new Error(`pocas velas (${bars.length})`);
        this.state.set(sym, { cur, triedAt: Date.now(), ...this.compute(bars) });
      } catch (e) {
        this.state.set(sym, { ...(s || {}), cur: s?.cur, triedAt: Date.now() });
        this.log('trend_error', { sym, error: e.message });
      }
    }
  }

  // velas de 1m cada minuto (5 s de margen); de ahi salen 3m y 5m
  async refreshCisd(meta) {
    const cur = Math.floor((Date.now() - 5000) / MIN) * MIN;
    for (const [sym, m] of Object.entries(meta)) {
      const s = this.cisd.get(sym);
      if (s && s.cur === cur) continue;
      if (s && Date.now() - s.triedAt < 15000) continue;
      try {
        const r = await this.stream.request('candles.history', { provider: m.provider, symbol: m.coin, interval: '1m', startTime: Date.now() - 2 * 86400000, endTime: Date.now(), limit: 1000 });
        const b1 = toBars(r).filter((b) => b.t < cur);
        if (b1.length < 200) throw new Error(`pocas velas de 1m (${b1.length})`);
        const tfs = {};
        for (const n of this.cfg.cisdTfs) {
          const a = analyze(aggMin(b1, n), { types: ['cisd'] });
          tfs[n] = a.last ? { dir: a.last.dir, t: a.last.t + n * MIN, level: a.last.level } : null; // t = cierre de la vela del CISD
        }
        const evs = Object.values(tfs).filter(Boolean);
        let dir = null;
        if (this.cfg.cisdMode === 'all') dir = evs.length === this.cfg.cisdTfs.length && evs.every((e) => e.dir === evs[0].dir) ? evs[0].dir : null;
        else dir = evs.sort((a, b) => b.t - a.t)[0]?.dir || null;
        const prev = s?.dir;
        this.cisd.set(sym, { cur, triedAt: Date.now(), lastBar: b1[b1.length - 1].t, tfs, dir });
        if (prev !== undefined && prev !== dir) this.log('cisd', { sym, dir, tfs });
      } catch (e) {
        this.cisd.set(sym, { ...(s || {}), cur: s?.cur, triedAt: Date.now() });
        this.log('trend_error', { sym, tf: '1m', error: e.message });
      }
    }
  }

  compute(bars) {
    const C = bars.map((b) => b.c);
    const last = bars[bars.length - 1];
    const s5 = analyze(bars);
    const s15 = analyze(agg(bars, 3));
    const ss = sessionStart(last.t + FIVE);
    const ses = bars.filter((b) => b.t >= ss);
    const vwap = ses.length ? ses.reduce((a, b) => a + (b.h + b.l + b.c) / 3, 0) / ses.length : null;
    return {
      lastBar: last.t, close: last.c,
      e9: ema(C, 9), e21: ema(C, 21), e20: ema(C, 20), e50: ema(C, 50), e200: ema(C, 200), vwap,
      s5: { trend: s5.trend, bias: s5.bias, last: s5.last && { type: s5.last.type, dir: s5.last.dir, t: s5.last.t } },
      s15: { trend: s15.trend, bias: s15.bias, last: s15.last && { type: s15.last.type, dir: s15.last.dir, t: s15.last.t } },
    };
  }

  // {ok, why, detail}: why lista los filtros que estan en contra
  check(sym, side) {
    if (!this.enabled()) return { ok: true };
    const want = side === 'short' ? 'down' : 'up';
    let cd = null;
    if (this.needCisd) {
      const c = this.cisd.get(sym);
      if (!c || c.lastBar == null) return { ok: false, why: 'sin velas de 1m para el CISD' };
      if (Date.now() - c.lastBar > 3 * MIN) return { ok: false, why: 'velas de 1m viejas' };
      const tf = Object.fromEntries(Object.entries(c.tfs).map(([n, e]) => [`${n}m`, e ? `${e.dir} ${new Date(e.t).toISOString().slice(11, 16)}` : null]));
      cd = { cisd: c.dir, ...tf };
      if (c.dir !== want) {
        const why = c.dir ? `en contra: CISD ${c.dir === 'up' ? 'alcista' : 'bajista'}` : 'CISD sin direccion';
        return { ok: false, why, detail: cd };
      }
      if (!this.need5) return { ok: true, detail: cd };
    }
    const s = this.state.get(sym);
    if (!s || s.lastBar == null) return { ok: false, why: 'sin velas para la tendencia' };
    if (Date.now() - s.lastBar > 3 * FIVE) return { ok: false, why: 'velas de tendencia viejas' };
    const dn = side === 'short';
    const res = {
      ema20_50: dn ? s.e20 < s.e50 : s.e20 > s.e50,
      ema200: dn ? s.close < s.e200 : s.close > s.e200,
      ema9_21: dn ? s.e9 < s.e21 : s.e9 > s.e21,
      struct5: allows({ ...s.s5, last: s.s5.last }, side, 'bias').ok,
      struct15: allows({ ...s.s15, last: s.s15.last }, side, 'bias').ok,
      vwap: s.vwap == null ? true : dn ? s.close < s.vwap : s.close > s.vwap,
    };
    res.cisd = true; // ya revisado arriba
    const bad = this.filters.filter((f) => !res[f]);
    const r2 = (x) => (x == null ? null : +x.toFixed(2));
    const detail = {
      ...(cd || {}),
      close: s.close, e20: r2(s.e20), e50: r2(s.e50), e200: r2(s.e200), vwap: r2(s.vwap),
      s5: s.s5.last ? `${s.s5.last.type} ${s.s5.last.dir}` : null, s15: s.s15.last ? `${s.s15.last.type} ${s.s15.last.dir}` : null,
    };
    const names = { ema20_50: 'EMA20/50', ema200: 'EMA200', ema9_21: 'EMA9/21', struct5: `estructura 5m (${detail.s5})`, struct15: `estructura 15m (${detail.s15})`, vwap: 'VWAP' };
    return bad.length ? { ok: false, why: 'en contra: ' + bad.map((f) => names[f]).join(', '), detail } : { ok: true, detail };
  }

  snapshot() {
    const out = {};
    const syms = new Set([...this.state.keys(), ...this.cisd.keys()]);
    for (const sym of syms) {
      out[sym] = { short: this.check(sym, 'short').ok, long: this.check(sym, 'long').ok, ...this.check(sym, 'short').detail };
    }
    return out;
  }
}
