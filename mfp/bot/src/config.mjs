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
  maxConcurrent: num('MAX_CONCURRENT', 5),
  // 0 = sin limite de entradas por dia (fase de pruebas)
  maxEntriesPerDay: num('MAX_ENTRIES_PER_DAY', 0),

  // Que zonas se operan
  grades: (env.GRADES || 'A+,A').split(',').map((s) => s.trim()),
  // Estados de zona que se operan. tocada/armada = re-test: el precio ya toco la zona, salio y puede volver.
  statuses: (env.ZONE_STATUSES || 'nueva,activa,tocada,armada').split(',').map((s) => s.trim()),
  minRR: num('MIN_RR', 1),
  maxDistAtr: num('MAX_DIST_ATR5', 6),
  maxFeedAgeMin: num('MAX_FEED_AGE_MIN', 5),
  // minutos sin poder bajar el plan de zonas antes de dejar de operar (con ZONES_FRESH=0 el plan se guarda cada 15 min)
  maxPlanAgeMin: num('MAX_PLAN_AGE_MIN', env.ZONES_FRESH === '0' ? 20 : 5),
  requireOperable: env.REQUIRE_OPERABLE !== '0',
  // Filtro de tendencia (src/trend.mjs): todos los de la lista deben estar a favor. Vacio = sin filtro.
  // Opciones: cisd, ema20_50, ema200, ema9_21, struct5, struct15, vwap. Por defecto ninguno: se operan las zonas tal cual.
  trendFilters: (env.TREND_FILTERS ?? '').split(',').map((s) => s.trim()).filter(Boolean),
  // filtro cisd: temporalidades (minutos) y modo. last = manda el CISD mas reciente de cualquiera; all = todas de acuerdo
  cisdTfs: (env.CISD_TFS ?? '1,3,5').split(',').map(Number).filter((n) => n > 0),
  cisdMode: env.CISD_MODE === 'all' ? 'all' : 'last',
  // una orden ya puesta solo se cancela por un CISD contrario en esta temporalidad (minutos), no por los cambios de 1m/3m
  cisdHoldTf: num('CISD_HOLD_TF', 5),
  // Racha de stops: SL_STREAK stops seguidos en la misma direccion, el primero y el ultimo a <= SL_STREAK_WINDOW_MIN,
  // bloquean esa direccion SL_BLOCK_MIN minutos (la otra direccion sigue). SL_BLOCK_SCOPE: market (por mercado) | all.
  slStreak: num('SL_STREAK', 2),
  slStreakWindowMin: num('SL_STREAK_WINDOW_MIN', 60),
  slBlockMin: num('SL_BLOCK_MIN', 120),
  slBlockScope: env.SL_BLOCK_SCOPE === 'all' ? 'all' : 'market',

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
  // 1 = pide el plan recalculado al momento (?fresh=1, con el estado en vivo del indicador de TradingView)
  // en vez del guardado por la corrida de cada 15 min
  zonesFresh: env.ZONES_FRESH !== '0',
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
