// fetch y WebSocket que respetan HTTPS_PROXY si existe (en un servidor normal no hace falta).
import { fetch as ufetch, EnvHttpProxyAgent } from 'undici';
import WebSocket from 'ws';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxy = process.env.HTTPS_PROXY || process.env.https_proxy || '';
const dispatcher = proxy ? new EnvHttpProxyAgent() : undefined;

export const fetch = (url, opts = {}) => ufetch(url, dispatcher ? { ...opts, dispatcher } : opts);

export const openWs = (url) =>
  new WebSocket(url, { perMessageDeflate: true, ...(proxy ? { agent: new HttpsProxyAgent(proxy) } : {}) });

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
