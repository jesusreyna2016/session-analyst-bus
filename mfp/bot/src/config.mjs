// Toda la configuracion sale de variables de entorno (ver .env.example).
const env = process.env;
const num = (k, d) => (env[k] !== undefined && env[k] !== '' ? Number(env[k]) : d);

export const SANDBOX = 'https://sandbox.myfundedperpetuals.com';
export const LIVE = 'https://developers.myfundedperpetuals.com';

export const cfg = {
  apiBase: env.MFP_API_BASE || SANDBOX,
  apiKey: env.MFP_API_KEY || '',
  accountId: env.MFP_ACCOUNT_ID || '',
  allowLive: env.ALLOW_LIVE === '1',
  streamUrl: env.MFP_STREAM_URL || 'wss://api-stream.myfundedperpetuals.com/v1/market-data',
  zonesUrl: env.ZONES_URL || 'https://tradedadlog.com/api/intraday-plan',

  // Riesgo (reglas de la cuenta real que se quiere imitar: 100K, DLL 3% = $3,000, drawdown $3,000)
  riskUsd: num('RISK_USD', 300),
  dllUsd: num('DLL_USD', 3000),
  dayStopPct: num('DAY_STOP_PCT', 0.9),
  maxDdUsd: num('MAX_DD_USD', 3000),
  maxConcurrent: num('MAX_CONCURRENT', 3),
  // 0 = sin limite de entradas por dia (fase de pruebas)
  maxEntriesPerDay: num('MAX_ENTRIES_PER_DAY', 0),

  // Que zonas se operan
  grades: (env.GRADES || 'A+,A').split(',').map((s) => s.trim()),
  minRR: num('MIN_RR', 1),
  maxDistAtr: num('MAX_DIST_ATR5', 6),
  maxFeedAgeMin: num('MAX_FEED_AGE_MIN', 5),
  requireOperable: env.REQUIRE_OPERABLE !== '0',

  // Diferencia perp - futuro
  basisMinSamples: num('BASIS_MIN_SAMPLES', 3),
  basisWindow: num('BASIS_WINDOW', 8),
  basisMaxSpreadR: num('BASIS_MAX_SPREAD_R', 0.2),
  basisMaxAgeMin: num('BASIS_MAX_AGE_MIN', 90),

  // Ordenes
  gtdMin: num('GTD_MIN', 30),
  renewMin: num('RENEW_MIN', 10),
  minGapR: num('MIN_GAP_R', 0.1),

  loopSec: num('LOOP_SEC', 15),
  zonesPollSec: num('ZONES_POLL_SEC', 60),
  reconcileSec: num('RECONCILE_SEC', 30),

  markets: JSON.parse(env.MARKETS || JSON.stringify({
    NQ: 'ostium|NDX',
    ES: 'ostium|SP500',
    GC: 'binance|XAUUSDT',
    ETHUSDT: 'binance|ETHUSDT',
    BTCUSDT: 'binance|BTCUSDT',
  })),

  dataDir: env.DATA_DIR || './data',
  port: num('PORT', 8080),
  dryRun: env.DRY_RUN === '1',
  cancelOnExit: env.CANCEL_ON_EXIT !== '0',

  gh: {
    token: env.GH_TOKEN || '',
    repo: env.GH_REPO || 'jesusreyna2016/session-analyst-bus',
    branch: env.GH_BRANCH || 'main',
    dir: env.GH_DIR || 'mfp/bot-data',
    everyMin: num('GH_EVERY_MIN', 10),
  },
};

export function assertSafe() {
  if (!cfg.apiKey) throw new Error('Falta MFP_API_KEY');
  if (cfg.apiBase !== SANDBOX && !cfg.allowLive) {
    throw new Error(`MFP_API_BASE=${cfg.apiBase} no es el sandbox. Para una cuenta real pon ALLOW_LIVE=1 a proposito.`);
  }
}
