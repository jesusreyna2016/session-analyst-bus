// Motor del bot: zonas de Mi Mesa -> ordenes limit en MFP con TP/SL, bajo las reglas de riesgo.
import fs from 'node:fs';
import path from 'node:path';
import { fetch } from './net.mjs';
import { Basis } from './basis.mjs';
import { Trend } from './trend.mjs';
import { dayUtc } from './journal.mjs';

const PREFIX = 'zb-';
const DEAD_STATUSES = new Set(['funciono', 'invalidada']);

const round = (x) => Number(x.toFixed(x >= 1000 ? 2 : x >= 10 ? 4 : 6));
const floorStep = (x, step) => { const n = Math.floor(x / step + 1e-9); return Number((n * step).toFixed(10)); };

export class Engine {
  constructor(cfg, mfp, stream, journal) {
    this.cfg = cfg;
    this.mfp = mfp;
    this.stream = stream;
    this.j = journal;
    this.log = (evt, data) => this.j.write(evt, data);
    this.basis = new Basis(cfg, this.log);
    this.trend = new Trend(cfg, { request: (...a) => this.stream.request(...a) }, this.log);
    const day = (ms) => new Date(ms).toISOString().slice(0, 10);
    const restored = this.basis.restore([...journal.read(day(Date.now() - 86400000)), ...journal.read(day(Date.now()))]);
    if (restored) console.log(`diferencia de precio: ${restored} muestras recuperadas de la bitacora`);
    this.plan = null;
    this.planAt = 0;
    this.acct = null;
    this.risk = null;
    this.status = { startedAt: new Date().toISOString() };
    this.statePath = path.join(cfg.dataDir, 'state.json');
    this.st = this.loadState();
    this.lastSkip = new Map();
    this.lastReconcile = 0;
  }

  loadState() {
    const d = { managed: {}, trades: {}, closedSeen: [], entriesToday: 0, dayStart: null, halted: false, blacklist: [], deadZones: [] };
    try { return { ...d, ...JSON.parse(fs.readFileSync(this.statePath, 'utf8')) }; } catch { return d; }
  }
  saveState() { fs.writeFileSync(this.statePath, JSON.stringify(this.st, null, 1)); }

  async init() {
    const accts = await this.mfp.accounts();
    const acct = this.cfg.accountId ? accts.find((a) => a.id === this.cfg.accountId || a.account_number === this.cfg.accountId) : accts.find((a) => a.status === 'active');
    if (!acct) throw new Error('No encontre la cuenta (MFP_ACCOUNT_ID) o no hay ninguna activa');
    if (acct.status !== 'active') throw new Error(`La cuenta ${acct.account_number} esta ${acct.status}`);
    this.acctId = acct.id;
    const all = await this.mfp.markets();
    this.meta = {};
    for (const [sym, mid] of Object.entries(this.cfg.markets)) {
      const m = all.find((x) => x.market_id === mid);
      if (!m) throw new Error(`Mercado ${mid} (${sym}) no existe en MFP`);
      this.meta[sym] = m;
    }
    const pol = await this.mfp.policy(this.acctId);
    this.log('start', {
      account: acct.account_number, accountId: acct.id, api: this.cfg.apiBase, dryRun: this.cfg.dryRun,
      markets: this.cfg.markets, rules: pol.account_rules, risk: { perTrade: this.cfg.riskUsd, dayStop: this.dayStopUsd(), maxDd: this.cfg.maxDdUsd },
      grades: this.cfg.grades,
    });
    return Object.values(this.meta);
  }

  dayStopUsd() { return this.cfg.dllUsd * this.cfg.dayStopPct; }

  // ---------- datos ----------
  async refreshPlan() {
    if (Date.now() - this.planAt < this.cfg.zonesPollSec * 1000 && this.plan) return;
    this.planAt = Date.now();
    try {
      const url = this.cfg.zonesFresh ? `${this.cfg.zonesUrl}?fresh=1` : this.cfg.zonesUrl;
      const r = await fetch(url, { signal: AbortSignal.timeout(20000) });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const p = await r.json();
      if (!p.symbols) throw new Error(p.error || 'plan sin simbolos');
      this.rememberDead(p);
      const changed = !this.plan || p.builtAt !== this.plan.builtAt;
      this.plan = p;
      if (changed) for (const sym of Object.keys(this.meta)) await this.basis.sample(sym, p, this.meta[sym], this.stream);
    } catch (e) {
      this.log('zones_error', { error: e.message });
    }
  }

  // Zonas que ya funcionaron o se invalidaron hoy: no se vuelven a operar aunque un recalculo
  // posterior las devuelva como activas (el plan al momento no siempre arrastra el estado).
  rememberDead(p) {
    const dead = this.st.deadZones;
    for (const [sym, s] of Object.entries(p.symbols || {})) {
      for (const z of s.zones || []) {
        if (!DEAD_STATUSES.has(z.status) || this.isDead(sym, z)) continue;
        dead.push({ sym, side: z.side, lo: z.lo, hi: z.hi, status: z.status, at: new Date().toISOString() });
      }
    }
    while (dead.length > 500) dead.shift();
  }

  isDead(sym, z) {
    return (this.st.deadZones || []).some((d) => d.sym === sym && d.side === z.side && d.lo <= z.hi && z.lo <= d.hi);
  }

  async refreshAccount() {
    const a = await this.mfp.account(this.acctId);
    const r = a.risk || {};
    const req = r.requirements || {};
    const start = a.starting_balance;
    const dayStart = r.daily_loss_floor + ((req.daily_loss_pct || 0) / 100) * start;
    if (this.st.dayStart !== null && Math.abs(dayStart - this.st.dayStart) > 0.01) {
      this.log('new_day', { prevDayStart: this.st.dayStart, dayStart, equity: r.equity });
      this.st.entriesToday = 0;
      this.st.halted = false;
      this.st.blacklist = [];
      this.st.deadZones = [];
    }
    this.st.dayStart = dayStart;
    const equity = r.equity;
    const dayLoss = Math.max(0, dayStart - equity);
    // drawdown estatico: piso duro = inicial - MAX_DD; el bot para al 90% (piso propio = inicial - 0.9*MAX_DD)
    const ddFloorHard = start - this.cfg.maxDdUsd;
    const ddFloorBot = start - this.cfg.maxDdUsd * this.cfg.dayStopPct;
    this.risk = {
      status: a.status, equity, dayStart, dayLoss,
      dayRoom: +(this.dayStopUsd() - dayLoss).toFixed(2),
      ddRoom: +(equity - ddFloorBot).toFixed(2),
      ddFloorHard, ddFloorBot, marksComplete: r.marks_complete,
    };
    if (a.status !== 'active') throw new Error(`cuenta ${a.status}`);
  }

  // ---------- riesgo ----------
  async checkHalt() {
    const r = this.risk;
    if (this.st.halted) return true;
    if (r.dayRoom <= 0 || r.ddRoom <= 0) {
      this.st.halted = true;
      this.log('halt', { reason: r.dayRoom <= 0 ? 'freno diario (90% del DLL)' : 'freno de drawdown (90%)', ...r });
      if (!this.cfg.dryRun) {
        await this.mfp.cancelAll(this.acctId).catch((e) => this.log('error', { where: 'cancelAll', error: e.message }));
        await this.mfp.closeAll(this.acctId).catch((e) => this.log('error', { where: 'closeAll', error: e.message }));
      }
      this.st.managed = {};
      this.saveState();
      return true;
    }
    return false;
  }

  skip(key, reason, extra = {}) {
    if (this.lastSkip.get(key) === reason) return;
    this.lastSkip.set(key, reason);
    this.log('skip', { zone: key, reason, ...extra });
  }

  // ---------- que ordenes deberian existir ----------
  desired(openMarkets, slots) {
    const out = [];
    const cfg = this.cfg;
    // si no se pudo bajar el plan hace rato, no se opera con zonas viejas (las ordenes en espera se cancelan)
    const planAgeMin = this.plan?.builtAt ? (Date.now() - Date.parse(this.plan.builtAt)) / 60000 : Infinity;
    if (planAgeMin > cfg.maxPlanAgeMin) { this.skip('plan', 'plan de zonas viejo', { planAgeMin: +planAgeMin.toFixed(1) }); return out; }
    for (const [sym, m] of Object.entries(this.meta)) {
      const s = this.plan?.symbols?.[sym];
      if (!s) continue;
      if (openMarkets.has(m.market_id)) continue; // una posicion por mercado
      if (Number(s.feedAgeMin ?? 99) > cfg.maxFeedAgeMin) { this.skip(sym, 'feed viejo', { feedAgeMin: s.feedAgeMin }); continue; }
      if (cfg.requireOperable && s.verdict !== 'OPERABLE') { this.skip(sym, `veredicto ${s.verdict}`); continue; }
      const b = this.basis.get(sym);
      const px = this.stream.price(m.market_id);
      let best = null;
      for (const z of s.zones || []) {
        const key = `${sym}|${z.id}`;
        if (!cfg.grades.includes(z.grade)) continue;
        if (!cfg.statuses.includes(z.status) || z.inside) continue;
        if (this.isDead(sym, z)) continue;
        if (this.st.blacklist.includes(key)) continue;
        if (!(z.rr1 >= cfg.minRR)) { this.skip(key, `rr1 ${z.rr1} < ${cfg.minRR}`); continue; }
        if (!(z.distAtr5 <= cfg.maxDistAtr)) continue; // lejos: aun no
        const tr = this.trend.check(sym, z.side);
        if (!tr.ok) { this.skip(key, tr.why, { trend: tr.detail }); continue; }
        if (!b.ready) { this.skip(key, `diferencia de precio sin datos (${b.n}/${cfg.basisMinSamples})`); continue; }
        const riskPts = Math.abs(z.entry - z.stop);
        if (b.spread > cfg.basisMaxSpreadR * riskPts) { this.skip(key, 'diferencia de precio inestable', { spread: b.spread, riskPts }); continue; }
        if (px === null) { this.skip(key, 'sin precio de MFP'); continue; }
        const long = z.side === 'long';
        const entry = round(z.entry + b.value);
        const stop = round(z.stop + b.value);
        const tp = round(z.tp1 + b.value);
        const gap = long ? px - entry : entry - px;
        if (gap < cfg.minGapR * riskPts) { this.skip(key, 'precio de MFP ya en la entrada', { px, entry }); continue; }
        const cand = { sym, key, zone: z, market: m, long, entry, stop, tp, basis: b.value, basisSpread: b.spread, px, trend: tr.detail };
        if (!best || z.score > best.zone.score) best = cand;
      }
      if (best) out.push(best);
    }
    out.sort((a, b) => b.zone.score - a.zone.score);
    return out.slice(0, Math.max(0, slots));
  }

  // ---------- ciclo ----------
  async tick() {
    await this.refreshPlan();
    await this.refreshAccount();
    await this.trend.refresh(this.meta);
    if (Date.now() - this.lastReconcile > this.cfg.reconcileSec * 1000) await this.reconcile();
    const halted = await this.checkHalt();

    const working = await this.mfp.workingOrders(this.acctId);
    const ours = working.filter((o) => (o.client_order_id || '').startsWith(PREFIX) && !o.reduce_only && o.type === 'limit');
    const open = await this.mfp.positions(this.acctId, 'open');
    const openMarkets = new Set(open.map((p) => p.market_id));
    const r = this.risk;

    // ordenes nuestras que ya no estan resting -> ver que paso
    const workingIds = new Set(ours.map((o) => o.client_order_id));
    for (const cid of Object.keys(this.st.managed)) if (!workingIds.has(cid)) await this.resolveGone(cid);

    const nOpen = open.length;
    const budget = Math.min(r.dayRoom, r.ddRoom) - nOpen * this.cfg.riskUsd;
    const slots = halted ? 0 : Math.min(
      this.cfg.maxConcurrent - nOpen,
      Math.floor(budget / this.cfg.riskUsd),
      this.cfg.maxEntriesPerDay > 0 ? this.cfg.maxEntriesPerDay - this.st.entriesToday : Infinity,
    );
    const want = halted ? [] : this.desired(openMarkets, slots);
    const wantByKey = new Map(want.map((w) => [w.key, w]));

    // cancelar lo que sobra o quedo viejo
    const keep = new Set();
    for (const o of ours) {
      const rec = this.st.managed[o.client_order_id];
      const w = rec && wantByKey.get(rec.key);
      let reason = null;
      if (!rec) reason = 'orden desconocida';
      else if (!w) reason = 'zona ya no elegible';
      else {
        const riskPts = Math.abs(w.entry - w.stop);
        if (Math.abs(w.entry - o.limit_price) > 0.05 * riskPts || Math.abs(w.stop - o.attached_stop_loss_price) > 0.05 * riskPts) reason = 'precios cambiaron';
        else if (o.gtd_expires_at && o.gtd_expires_at - Date.now() < this.cfg.renewMin * 60000) reason = 'renovar';
      }
      if (reason) await this.cancel(o, rec, reason);
      else keep.add(rec.key);
    }
    for (const w of want) if (!keep.has(w.key)) await this.place(w);

    this.status = {
      ...this.status, at: new Date().toISOString(), halted: this.st.halted, risk: r, entriesToday: this.st.entriesToday,
      planBuiltAt: this.plan?.builtAt, basis: this.basis.snapshot(), trend: this.trend.snapshot(), trendFilters: this.cfg.trendFilters,
      resting: Object.values(this.st.managed).map((m) => ({ sym: m.sym, zone: m.zoneId, side: m.side, entry: m.entry, stop: m.stop, tp: m.tp, size: m.size })),
      open: open.map((p) => ({ market: p.market_id, side: p.side, size: p.size, entry: p.entry_price })),
    };
    this.saveState();
  }

  async place(w) {
    const { market: m, zone: z } = w;
    const dist = Math.abs(w.entry - w.stop);
    let feeRate = m.provider === 'binance' && /USDT$/.test(m.coin) && !/^(XAU|XAG|CL|NATGAS|QQQ)/.test(m.coin) ? 0.0003 : 0.00005;
    try {
      const q = await this.mfp.quote(m.market_id, w.long ? 'buy' : 'sell', floorStep(this.cfg.riskUsd / dist, m.size_step) || m.min_size);
      if (q.estimated_fee && q.estimated_notional) feeRate = q.estimated_fee / q.estimated_notional;
    } catch { /* usamos la tabla */ }
    const perUnit = dist + w.entry * feeRate * 2;
    const size = floorStep(this.cfg.riskUsd / perUnit, m.size_step);
    const notional = size * w.entry;
    if (size < m.min_size || notional < m.min_notional) { this.skip(w.key, 'tamano minimo', { size }); return; }
    const cid = `${PREFIX}${w.sym}-${w.zone.side[0]}${String(z.entry).replace(/[^0-9]/g, '')}-${Date.now().toString(36)}`;
    const order = {
      client_order_id: cid, type: 'limit', account_id: this.acctId, market_id: m.market_id,
      side: w.long ? 'buy' : 'sell', size, limit_price: w.entry, leverage: m.max_leverage, margin_mode: 'cross',
      time_in_force: 'gtd', gtd_expires_at: Date.now() + this.cfg.gtdMin * 60000,
      take_profit_price: w.tp, stop_loss_price: w.stop,
    };
    const rec = {
      cid, key: w.key, sym: w.sym, zoneId: z.id, zoneStatus: z.status, grade: z.grade, score: z.score, aligned: z.aligned, rr1: z.rr1,
      side: z.side, marketId: m.market_id, size, notional: +notional.toFixed(2), feeRate,
      fut: { entry: z.entry, stop: z.stop, tp1: z.tp1, lo: z.lo, hi: z.hi }, basis: +w.basis.toFixed(4), basisSpread: +w.basisSpread.toFixed(4),
      entry: w.entry, stop: w.stop, tp: w.tp, pxAtPlace: w.px, plannedRiskUsd: +(size * perUnit).toFixed(2),
      planBuiltAt: this.plan?.builtAt, placedAt: Date.now(), trend: w.trend || null,
    };
    if (this.cfg.dryRun) { this.log('place_dry', rec); return; }
    try {
      const o = await this.mfp.placeOrder(order, cid);
      rec.orderId = o.id;
      this.st.managed[cid] = rec;
      this.log('place', rec);
    } catch (e) {
      this.log('place_error', { ...rec, status: e.status, code: e.code, error: e.message });
      if (e.status >= 400 && e.status < 500 && e.status !== 429) this.st.blacklist.push(w.key);
    }
  }

  async cancel(o, rec, reason) {
    if (this.cfg.dryRun) return;
    try {
      await this.mfp.cancelOrder(o.id);
      this.log('cancel', { cid: o.client_order_id, sym: rec?.sym, zone: rec?.zoneId, reason });
    } catch (e) {
      this.log('error', { where: 'cancel', cid: o.client_order_id, error: e.message });
    }
    // si se lleno mientras cancelabamos, resolveGone lo vera en el siguiente ciclo
  }

  async resolveGone(cid) {
    const rec = this.st.managed[cid];
    let o = null;
    try { const r = await this.mfp.orderByClientId(this.acctId, cid); o = Array.isArray(r) ? r[0] : r; } catch (e) { return; }
    if (!o) { delete this.st.managed[cid]; return; }
    if (o.status === 'resting' || o.status === 'pending') return;
    delete this.st.managed[cid];
    if (o.filled_size > 0 || o.status === 'filled') {
      this.st.entriesToday += 1;
      this.st.trades[cid] = { ...rec, filledAt: Date.now(), orderStatus: o.status, fillPrice: o.fill_price ?? o.limit_price, filledSize: o.filled_size };
      this.log('entry_filled', { cid, sym: rec.sym, zone: rec.zoneId, side: rec.side, limit: rec.entry, fill: o.fill_price ?? null, size: o.filled_size || o.size || rec.size, status: o.status });
    } else if (o.status !== 'canceled') {
      this.log('order_end', { cid, sym: rec?.sym, zone: rec?.zoneId, status: o.status, reason: o.cancel_reason || o.reject_reason || null, rule: o.reject_rule_id || null });
    }
  }

  // posiciones cerradas -> resultado del trade
  async reconcile() {
    this.lastReconcile = Date.now();
    let page;
    try { page = await this.mfp.positions(this.acctId, 'closed'); } catch (e) { this.log('error', { where: 'closed positions', error: e.message }); return; }
    const items = page.json?.data || [];
    const seen = new Set(this.st.closedSeen);
    for (const p of items) {
      if (seen.has(p.id)) continue;
      const t = Object.values(this.st.trades).find((x) => !x.closed && x.marketId === p.market_id && p.opened_at >= x.placedAt - 60000);
      this.st.closedSeen.push(p.id);
      if (!t) continue;
      t.closed = true;
      const realized = Number(p.realized_pnl ?? 0);
      const fees = Number(p.fees ?? 0);
      const funding = Number(p.funding ?? 0);
      // realized_pnl de MFP es bruto (sin comisiones): el neto descuenta las comisiones
      const net = realized - fees;
      const exitTarget = p.close_reason;
      const slipExit = p.exit_price != null
        ? (t.side === 'long' ? 1 : -1) * (p.exit_price - (Math.abs(p.exit_price - t.stop) < Math.abs(p.exit_price - t.tp) ? t.stop : t.tp))
        : null;
      this.log('trade_closed', {
        cid: t.cid, sym: t.sym, zone: t.zoneId, grade: t.grade, side: t.side, positionId: p.id,
        entryPlanned: t.entry, entryFill: p.entry_price, exitPrice: p.exit_price, stop: t.stop, tp: t.tp,
        closeReason: exitTarget, realizedPnl: realized, fees, funding, netPnl: +net.toFixed(4),
        R: +(net / this.cfg.riskUsd).toFixed(3), Rgross: +(realized / this.cfg.riskUsd).toFixed(3), slipEntry: p.entry_price != null ? +((t.side === 'long' ? 1 : -1) * (t.entry - p.entry_price)).toFixed(4) : null,
        slipExit: slipExit != null ? +slipExit.toFixed(4) : null, heldMin: p.closed_at && p.opened_at ? Math.round((p.closed_at - p.opened_at) / 60000) : null,
        raw: p,
      });
    }
    if (this.st.closedSeen.length > 2000) this.st.closedSeen = this.st.closedSeen.slice(-1000);
  }

  async shutdown() {
    if (!this.cfg.cancelOnExit || this.cfg.dryRun) return;
    for (const rec of Object.values(this.st.managed)) {
      if (rec.orderId) await this.mfp.cancelOrder(rec.orderId).catch(() => {});
    }
    this.log('stop', { canceled: Object.keys(this.st.managed).length });
    this.st.managed = {};
    this.saveState();
  }
}

export { dayUtc };
