// Cliente REST de MyFundedPerps (solo lo que usa el bot).
import crypto from 'node:crypto';
import { fetch, sleep } from './net.mjs';

export class MfpError extends Error {
  constructor(msg, status, body) {
    super(msg);
    this.status = status;
    this.body = body;
    this.code = body?.error?.code || body?.code || null;
  }
}

export class Mfp {
  constructor({ apiBase, apiKey }) {
    this.base = apiBase.replace(/\/$/, '');
    this.key = apiKey;
  }

  async req(method, path, { body, query, idem, raw = false } = {}) {
    const url = new URL(this.base + path);
    for (const [k, v] of Object.entries(query || {})) if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
    const key = idem || (method === 'POST' ? crypto.randomUUID() : undefined);
    for (let attempt = 0; ; attempt++) {
      const headers = { Authorization: `Bearer ${this.key}`, Accept: 'application/json' };
      if (body) headers['Content-Type'] = 'application/json';
      if (key) headers['Idempotency-Key'] = key;
      let res;
      try {
        res = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(20000) });
      } catch (e) {
        if (attempt < 4) { await sleep(1000 * 2 ** attempt); continue; }
        throw new MfpError(`${method} ${path}: ${e.message}`, 0, null);
      }
      const text = await res.text();
      let json = null;
      try { json = text ? JSON.parse(text) : null; } catch { json = { text }; }
      if ((res.status === 429 || res.status === 503 || res.status >= 500) && attempt < 4) {
        const ra = Number(res.headers.get('retry-after'));
        await sleep(Number.isFinite(ra) && ra > 0 ? ra * 1000 : 1000 * 2 ** attempt);
        continue;
      }
      if (!res.ok) {
        const m = json?.error?.message || json?.message || text.slice(0, 300);
        throw new MfpError(`${method} ${path} -> ${res.status}: ${m}`, res.status, json);
      }
      if (raw) return { status: res.status, json, retryAfter: Number(res.headers.get('retry-after')) || 1 };
      return json && 'data' in json ? json.data : json;
    }
  }

  accounts() { return this.req('GET', '/v1/accounts'); }
  account(id) { return this.req('GET', `/v1/accounts/${id}`); }
  policy(id) { return this.req('GET', `/v1/accounts/${id}/trading-policy`); }
  markets() { return this.req('GET', '/v1/markets', { query: { venues: 'all' } }); }
  quote(marketId, side, size) {
    return this.req('GET', `/v1/markets/${encodeURIComponent(marketId)}/quote`, { query: { side, size } });
  }
  workingOrders(accountId) { return this.req('GET', '/v1/orders', { query: { account_id: accountId, status: 'working' } }); }
  orderByClientId(accountId, cid) { return this.req('GET', '/v1/orders', { query: { account_id: accountId, client_order_id: cid } }); }
  placeOrder(order, idem) { return this.req('POST', '/v1/orders', { body: order, idem }); }
  cancelOrder(id) { return this.req('DELETE', `/v1/orders/${id}`); }
  positions(accountId, status = 'open', cursor) {
    return this.req('GET', '/v1/positions', { query: { account_id: accountId, status, cursor, limit: status === 'closed' ? 50 : undefined }, raw: status === 'closed' });
  }
  fills(accountId, cursor) { return this.req('GET', '/v1/fills', { query: { account_id: accountId, cursor, limit: 50 }, raw: true }); }

  // cancel-all / close-all avanzan por partes: se repite con la misma Idempotency-Key hasta 'completed'
  async untilDone(path) {
    const idem = crypto.randomUUID();
    for (let i = 0; i < 30; i++) {
      const r = await this.req('POST', path, { idem, raw: true });
      if (r.status !== 202) return r.json;
      await sleep(r.retryAfter * 1000);
    }
    throw new MfpError(`${path}: no termino`, 0, null);
  }
  cancelAll(accountId) { return this.untilDone(`/v1/accounts/${accountId}/cancel-all-orders`); }
  closeAll(accountId) { return this.untilDone(`/v1/accounts/${accountId}/close-all-positions`); }
}
