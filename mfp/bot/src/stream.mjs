// WebSocket publico de mercado de MFP: ultimo precio (mid/mark) por mercado + historial de velas a pedido.
import { openWs, sleep } from './net.mjs';

export class MarketStream {
  constructor(url, markets, log) {
    this.url = url;
    this.markets = markets; // [{market_id, provider, coin}]
    this.log = log;
    this.px = new Map(); // market_id -> {price, kind, time}
    this.ws = null;
    this.nextId = 1;
    this.pending = new Map();
    this.closed = false;
    this.lastMsg = 0;
  }

  key(provider, coin) { return `${provider}|${coin}`; }

  start() {
    this.byKey = new Map(this.markets.map((m) => [this.key(m.provider, m.coin), m.market_id]));
    this.connect();
    this.watchdog = setInterval(() => {
      if (this.ws && Date.now() - this.lastMsg > 90000) { this.log('stream', { msg: 'sin datos 90s, reconecto' }); this.ws.terminate(); }
    }, 30000);
  }

  connect() {
    if (this.closed) return;
    const ws = openWs(this.url);
    this.ws = ws;
    ws.on('open', () => {
      this.fails = 0;
      this.lastMsg = Date.now();
      const byProv = {};
      for (const m of this.markets) (byProv[m.provider] ||= []).push(m.coin);
      for (const [provider, symbols] of Object.entries(byProv)) {
        ws.send(JSON.stringify({ op: 'sub', id: this.nextId++, channel: 'ticks', payload: { symbols, providers: [provider] } }));
      }
      this.log('stream', { msg: 'conectado', providers: Object.keys(byProv) });
    });
    ws.on('message', (data) => {
      this.lastMsg = Date.now();
      let f;
      try { f = JSON.parse(data); } catch { return; }
      if (f.op === 'events') {
        for (const e of f.events || []) {
          if (e.type !== 'tick' && !('kind' in e)) continue;
          const mid = this.byKey.get(this.key(e.provider, e.symbol));
          if (!mid) continue;
          const prev = this.px.get(mid);
          // preferimos mid; mark si no hay mid reciente
          if (e.kind === 'mid' || !prev || prev.kind !== 'mid' || Date.now() - prev.at > 10000) {
            this.px.set(mid, { price: Number(e.price), kind: e.kind, time: e.time, at: Date.now() });
          }
        }
      } else if (f.op === 'res' || f.op === 'err') {
        const p = this.pending.get(f.id);
        if (p) { this.pending.delete(f.id); f.op === 'res' ? p.res(f.result) : p.rej(new Error(JSON.stringify(f.error))); }
      } else if (f.op === 'draining' || f.op === 'end') {
        ws.terminate();
      } else if (f.op === 'sub_err') {
        this.log('stream', { msg: 'sub_err', error: f.error });
      }
    });
    ws.on('close', async () => {
      for (const p of this.pending.values()) p.rej(new Error('ws cerrado'));
      this.pending.clear();
      if (this.closed) return;
      // espera creciente (3 s, 6 s, 12 s ... hasta 2 min) para no caer en el limite de conexiones de MFP (429)
      this.fails = (this.fails || 0) + 1;
      const wait = Math.min(120000, 3000 * 2 ** (this.fails - 1));
      if (this.fails > 1) this.log('stream', { msg: 'reconecto', inSec: wait / 1000, tries: this.fails });
      await sleep(wait);
      this.connect();
    });
    ws.on('error', (e) => this.log('stream', { msg: 'error', error: e.message }));
  }

  price(marketId, maxAgeMs = 30000) {
    const p = this.px.get(marketId);
    return p && Date.now() - p.at <= maxAgeMs ? p.price : null;
  }

  request(method, payload, timeoutMs = 20000) {
    return new Promise((res, rej) => {
      if (!this.ws || this.ws.readyState !== 1) return rej(new Error('ws no conectado'));
      const id = this.nextId++;
      const t = setTimeout(() => { this.pending.delete(id); rej(new Error('timeout')); }, timeoutMs);
      this.pending.set(id, { res: (v) => { clearTimeout(t); res(v); }, rej: (e) => { clearTimeout(t); rej(e); } });
      this.ws.send(JSON.stringify({ op: 'req', id, method, payload }));
    });
  }

  // cierre de la vela de 1m que contiene el instante t (ms)
  async closeAt(market, t) {
    const open = Math.floor(t / 60000) * 60000;
    const r = await this.request('candles.history', {
      provider: market.provider, symbol: market.coin, interval: '1m', startTime: open - 120000, endTime: open + 60000, limit: 5,
    });
    const c = (r || []).find((x) => x.openTime === open) || (r || []).filter((x) => x.openTime <= open).pop();
    return c ? Number(c.close) : null;
  }

  stop() { this.closed = true; clearInterval(this.watchdog); this.ws?.terminate(); }
}
