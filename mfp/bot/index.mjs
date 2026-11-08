// mfp-zone-bot
//   node index.mjs          -> corre el bot (ciclo cada LOOP_SEC, /health y /status en PORT)
//   node index.mjs check    -> verifica cuenta, mercados, zonas y stream sin poner ordenes
//   node index.mjs report [YYYY-MM-DD] [YYYY-MM-DD]  -> reporte zona vs ejecucion
import http from 'node:http';
import { cfg, assertSafe } from './src/config.mjs';
import { Mfp } from './src/mfp.mjs';
import { MarketStream } from './src/stream.mjs';
import { Journal, dayUtc } from './src/journal.mjs';
import { Engine } from './src/engine.mjs';
import { buildReport } from './src/report.mjs';
import { sleep } from './src/net.mjs';

const cmd = process.argv[2] || 'run';
const journal = new Journal(cfg);

async function main() {
  if (cmd === 'report') {
    const from = process.argv[3] || dayUtc();
    const to = process.argv[4] || from;
    const days = [];
    for (let t = Date.parse(from); t <= Date.parse(to); t += 86400000) days.push(dayUtc(t));
    const md = await buildReport(cfg, journal, days);
    journal.writeFile(`report-${from}${to !== from ? '_' + to : ''}.md`, md);
    console.log(md);
    await journal.syncGithub();
    return;
  }

  assertSafe();
  const mfp = new Mfp(cfg);
  const log = (evt, data) => journal.write(evt, data);
  const engine = new Engine(cfg, mfp, null, journal);
  const markets = await engine.init();
  const stream = new MarketStream(cfg.streamUrl, markets, log);
  engine.stream = stream;
  stream.start();
  await sleep(4000);

  if (cmd === 'check') {
    await engine.refreshPlan();
    await engine.refreshAccount();
    console.log('riesgo', engine.risk);
    for (const [sym, m] of Object.entries(engine.meta)) {
      const s = engine.plan?.symbols?.[sym];
      console.log(sym, m.market_id, 'MFP', stream.price(m.market_id), '| futuro', s?.price, 'feedAgeMin', s?.feedAgeMin, s?.verdict,
        '| basis', JSON.stringify(engine.basis.get(sym)), '| zonas', (s?.zones || []).map((z) => `${z.grade}/${z.status}/${z.side}@${z.entry}`).join(' '));
    }
    stream.stop();
    return;
  }

  const server = http.createServer((req, res) => {
    const body = req.url.startsWith('/status') ? engine.status : { ok: true, at: engine.status.at, halted: engine.st.halted };
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(body, null, 1));
  }).listen(cfg.port);

  let stopping = false;
  const stop = async (sig) => {
    if (stopping) return;
    stopping = true;
    log('signal', { sig });
    await engine.shutdown().catch((e) => console.error(e));
    stream.stop();
    server.close();
    await journal.syncGithub();
    process.exit(0);
  };
  process.on('SIGINT', () => stop('SIGINT'));
  process.on('SIGTERM', () => stop('SIGTERM'));

  let lastSync = Date.now();
  let lastReportDay = dayUtc();
  let errors = 0;
  while (!stopping) {
    try {
      await engine.tick();
      errors = 0;
    } catch (e) {
      errors++;
      log('error', { where: 'tick', error: e.message, n: errors });
      if (/cuenta (failed|passed|inactive)/.test(e.message)) { log('fin', { reason: e.message }); break; }
      await sleep(Math.min(60000, 2000 * errors));
    }
    if (dayUtc() !== lastReportDay) {
      const md = await buildReport(cfg, journal, [lastReportDay]).catch((e) => `error: ${e.message}`);
      journal.writeFile(`report-${lastReportDay}.md`, md);
      lastReportDay = dayUtc();
    }
    if (Date.now() - lastSync > cfg.gh.everyMin * 60000) { lastSync = Date.now(); await journal.syncGithub(); }
    await sleep(cfg.loopSec * 1000);
  }
  await stop('fin');
}

main().catch((e) => {
  console.error('FATAL', e.message);
  journal.write('fatal', { error: e.message });
  process.exit(1);
});
