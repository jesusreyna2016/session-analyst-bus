// Reporte: que tan buenas fueron las zonas y que tan bien se ejecutaron en MFP.
import { fetch } from './net.mjs';

const pct = (a, b) => (b ? `${Math.round((100 * a) / b)}%` : '—');
const f2 = (x) => (x == null || Number.isNaN(x) ? '—' : (+x).toFixed(2));
const ctDay = (ms) => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Chicago' }).format(new Date(ms));

export async function buildReport(cfg, journal, days) {
  const ev = days.flatMap((d) => journal.read(d));
  const places = ev.filter((e) => e.evt === 'place');
  const fills = ev.filter((e) => e.evt === 'entry_filled');
  const closed = ev.filter((e) => e.evt === 'trade_closed');
  const errors = ev.filter((e) => e.evt === 'place_error' || e.evt === 'order_end');
  const halts = ev.filter((e) => e.evt === 'halt');
  const skips = ev.filter((e) => e.evt === 'skip');

  // resultado final de cada zona segun Mi Mesa (registro del dia, hora Chicago)
  const ctDays = [...new Set(places.map((p) => ctDay(Date.parse(p.ts))))];
  const zoneLog = new Map();
  for (const d of ctDays) {
    try {
      const r = await fetch(`${cfg.zonesUrl}?log=${d}`, { signal: AbortSignal.timeout(20000) });
      const j = await r.json();
      for (const z of j.zones || []) zoneLog.set(`${z.sym}|${z.id}`, z.status);
    } catch { /* sin log */ }
  }

  const zonesPlaced = new Map();
  for (const p of places) if (!zonesPlaced.has(p.key)) zonesPlaced.set(p.key, p);
  const filledKeys = new Set(fills.map((f) => `${f.sym}|${f.zone}`));

  const L = [];
  L.push(`# Bot de zonas en MFP · ${days[0]}${days.length > 1 ? ` → ${days[days.length - 1]}` : ''}\n`);
  const R = closed.map((c) => c.R);
  const wins = closed.filter((c) => c.realizedPnl > 0).length;
  const pnl = closed.reduce((a, c) => a + c.realizedPnl, 0);
  const fees = closed.reduce((a, c) => a + (c.fees || 0), 0);
  const funding = closed.reduce((a, c) => a + (c.funding || 0), 0);
  L.push('## Resumen\n');
  L.push(`| | |\n|---|---|`);
  L.push(`| Zonas con orden puesta | ${zonesPlaced.size} |`);
  L.push(`| Se llenaron | ${fills.length} (${pct(fills.length, zonesPlaced.size)}) |`);
  L.push(`| Trades cerrados | ${closed.length} · ganados ${wins} (${pct(wins, closed.length)}) |`);
  L.push(`| Resultado | ${f2(pnl)} USD · ${f2(R.reduce((a, b) => a + b, 0))}R · promedio ${f2(R.length ? R.reduce((a, b) => a + b, 0) / R.length : null)}R |`);
  L.push(`| Comisiones / swap reportados | ${f2(fees)} / ${f2(funding)} USD |`);
  L.push(`| Rechazos o vencidas | ${errors.length} |`);
  L.push(`| Frenos de riesgo | ${halts.length} |`);

  // zona vs ejecucion
  L.push('\n## Zona vs ejecución\n');
  L.push('Resultado de la zona según Mi Mesa (en futuros) contra lo que pasó en MFP.\n');
  L.push('| zona | grado | Mi Mesa dice | MFP | R | entrada plan → real | salida | basis |');
  L.push('|---|---|---|---|---|---|---|---|');
  let agree = 0, comparable = 0;
  for (const c of closed) {
    const p = zonesPlaced.get(`${c.sym}|${c.zone}`) || {};
    const zs = zoneLog.get(`${c.sym}|${c.zone}`) || '¿?';
    const mfpRes = c.realizedPnl > 0 ? 'ganó' : 'perdió';
    if (zs === 'funciono' || zs === 'invalidada') { comparable++; if ((zs === 'funciono') === (c.realizedPnl > 0)) agree++; }
    L.push(`| ${c.sym} ${c.zone} | ${c.grade} | ${zs} | ${mfpRes} (${c.closeReason || '—'}) | ${f2(c.R)} | ${f2(c.entryPlanned)} → ${f2(c.entryFill)} | ${f2(c.exitPrice)} | ${f2(p.basis)} |`);
  }
  L.push(`\nCoinciden zona y ejecución en ${agree} de ${comparable} trades comparables.`);

  // zonas que funcionaron y no se operaron
  const missed = [...zoneLog.entries()].filter(([k, s]) => s === 'funciono' && !filledKeys.has(k));
  const graded = missed.filter(([k]) => zonesPlaced.has(k) || skips.some((s) => s.zone === k));
  L.push(`\n## Zonas que funcionaron sin trade\n\n${missed.length} en el registro de Mi Mesa (todas las calificaciones); ${graded.length} eran candidatas del bot.`);
  const reasons = {};
  for (const [k] of graded) {
    const s = [...skips].reverse().find((x) => x.zone === k);
    const why = zonesPlaced.has(k) ? 'orden puesta, no se llenó en MFP' : s?.reason || 'otra';
    reasons[why] = (reasons[why] || 0) + 1;
  }
  for (const [k, v] of Object.entries(reasons)) L.push(`- ${k}: ${v}`);

  if (errors.length) {
    L.push('\n## Rechazos\n');
    for (const e of errors.slice(0, 30)) L.push(`- ${e.ts} ${e.sym} ${e.zone || e.zoneId || ''}: ${e.code || e.status || ''} ${e.reason || e.error || ''}`);
  }
  return L.join('\n') + '\n';
}
