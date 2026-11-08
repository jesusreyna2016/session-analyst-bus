// Diferencia perp MFP - futuro, recalculada en vivo.
// Cada vez que el plan intradia cambia (cada 15 min) tomamos el precio del futuro que trae
// (sym.price, con feedAgeMin de antiguedad) y el cierre de la vela de 1m de MFP en ese mismo minuto.
// La diferencia vigente es la mediana de las ultimas BASIS_WINDOW muestras.

const median = (a) => { const s = [...a].sort((x, y) => x - y); const n = s.length; return n ? (n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2) : null; };

export class Basis {
  constructor(cfg, log) {
    this.cfg = cfg;
    this.log = log;
    this.samples = new Map(); // sym -> [{t, fut, perp, d}]
    this.seen = new Set();
  }

  async sample(sym, plan, market, stream) {
    const s = plan.symbols?.[sym];
    if (!s || !Number.isFinite(s.price)) return;
    const age = Number(s.feedAgeMin ?? 99);
    if (age > this.cfg.maxFeedAgeMin) return;
    // sym.price es el CIERRE de la vela de 5m que termina en t (alerta de TradingView al cierre).
    // t = la marca de 5m anterior a (builtAt - feedAgeMin). Se compara con el minuto de MFP que cierra en t.
    const t = Math.floor((Date.parse(plan.builtAt) - age * 60000) / 300000) * 300000;
    const key = `${sym}|${t}`;
    if (this.seen.has(key)) return;
    this.seen.add(key);
    let perp = null;
    try { perp = await stream.closeAt(market, t - 30000); } catch (e) { this.log('basis_error', { sym, error: e.message }); return; }
    if (!Number.isFinite(perp)) return;
    const d = perp - s.price;
    const arr = this.samples.get(sym) || [];
    arr.push({ t, fut: s.price, perp, d });
    while (arr.length > this.cfg.basisWindow) arr.shift();
    this.samples.set(sym, arr);
    this.log('basis_sample', { sym, t: new Date(t).toISOString(), fut: s.price, perp, d: +d.toFixed(4), med: +median(arr.map((x) => x.d)).toFixed(4), n: arr.length });
  }

  // {value, spread, n} o null si no hay suficientes muestras recientes
  get(sym) {
    const cutoff = Date.now() - this.cfg.basisMaxAgeMin * 60000;
    const arr = (this.samples.get(sym) || []).filter((x) => x.t >= cutoff);
    if (arr.length < this.cfg.basisMinSamples) return { ready: false, n: arr.length };
    const ds = arr.map((x) => x.d);
    return { ready: true, value: median(ds), spread: Math.max(...ds) - Math.min(...ds), n: arr.length };
  }

  snapshot() {
    const out = {};
    for (const sym of this.samples.keys()) out[sym] = this.get(sym);
    return out;
  }
}
