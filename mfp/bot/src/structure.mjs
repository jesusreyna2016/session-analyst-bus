// Estructura de mercado sobre velas (de MFP): detecta cambios de tendencia.
//
// Eventos (cada uno con direccion 'up' | 'down'):
//   bos   - cierre que rompe el ultimo swing a favor de la tendencia
//   choch - cierre que rompe el ultimo swing EN CONTRA de la tendencia (cambio de caracter / MSS)
//   cisd  - cierre que pasa la apertura de la ultima serie de velas contrarias (change in state of delivery)
//   ifvg  - cierre que atraviesa un FVG contrario (FVG invertido)
//
// trend = direccion de la ultima ruptura de estructura (bos/choch); bias = direccion del ultimo evento de cualquier tipo.
// Un short se bloquea si el sesgo (o la tendencia, segun el modo) es alcista, y al reves para un long.

const ALL = ['bos', 'choch', 'cisd', 'ifvg'];

export function toBars(candles) {
  return (candles || [])
    .filter((c) => c.isFinal !== false)
    .map((c) => ({ t: c.openTime, o: +c.open, h: +c.high, l: +c.low, c: +c.close }))
    .sort((a, b) => a.t - b.t);
}

export function analyze(bars, opt = {}) {
  const L = opt.pivot ?? 2; // velas a cada lado para confirmar un swing
  const minRun = opt.cisdRun ?? 2; // velas seguidas que forman la serie del CISD
  const fvgMaxAge = opt.fvgMaxAge ?? 48;
  const fvgMinAtr = opt.fvgMinAtr ?? 0.15;
  const types = new Set(opt.types || ALL);

  const events = [];
  let trend = null;
  let swingH = null; let swingL = null;
  let fvgs = [];
  // CISD: apertura de la primera vela de la ultima serie bajista (nivel para el CISD alcista) y viceversa
  let run = { dir: null, len: 0, open: null };
  let cisdUp = null; let cisdDn = null;
  let atr = null;

  const push = (type, dir, i, level) => { if (types.has(type)) events.push({ type, dir, t: bars[i].t, i, level, close: bars[i].c }); };

  for (let i = 0; i < bars.length; i++) {
    const b = bars[i];
    const tr = i ? Math.max(b.h - b.l, Math.abs(b.h - bars[i - 1].c), Math.abs(b.l - bars[i - 1].c)) : b.h - b.l;
    atr = atr == null ? tr : atr + (tr - atr) / 14;

    // swing confirmado en i-L
    const p = i - L;
    if (p - L >= 0) {
      let isH = true; let isL = true;
      for (let k = p - L; k <= p + L; k++) {
        if (k === p) continue;
        if (bars[k].h >= bars[p].h) isH = false;
        if (bars[k].l <= bars[p].l) isL = false;
      }
      if (isH) swingH = { price: bars[p].h, i: p, broken: false };
      if (isL) swingL = { price: bars[p].l, i: p, broken: false };
    }

    // ruptura de estructura
    if (swingH && !swingH.broken && b.c > swingH.price) {
      push(trend === 'down' ? 'choch' : 'bos', 'up', i, swingH.price);
      trend = 'up'; swingH.broken = true;
    }
    if (swingL && !swingL.broken && b.c < swingL.price) {
      push(trend === 'up' ? 'choch' : 'bos', 'down', i, swingL.price);
      trend = 'down'; swingL.broken = true;
    }

    // CISD
    if (cisdUp != null && b.c > cisdUp) { push('cisd', 'up', i, cisdUp); cisdUp = null; }
    if (cisdDn != null && b.c < cisdDn) { push('cisd', 'down', i, cisdDn); cisdDn = null; }
    const dir = b.c > b.o ? 'up' : b.c < b.o ? 'down' : null;
    if (dir) {
      if (dir === run.dir) run.len++;
      else {
        // termino una serie: su apertura queda como nivel del CISD contrario
        if (run.len >= minRun) { if (run.dir === 'down') cisdUp = run.open; else cisdDn = run.open; }
        run = { dir, len: 1, open: b.o };
      }
    }

    // IFVG: un cierre que atraviesa un FVG contrario
    fvgs = fvgs.filter((g) => {
      if (i - g.i > fvgMaxAge) return false;
      if (i === g.i) return true;
      if (g.dir === 'down' && b.c > g.top) { push('ifvg', 'up', i, g.top); return false; }
      if (g.dir === 'up' && b.c < g.bot) { push('ifvg', 'down', i, g.bot); return false; }
      return true;
    });
    if (i >= 2) {
      const a = bars[i - 2];
      if (b.l > a.h && b.l - a.h >= fvgMinAtr * atr) fvgs.push({ dir: 'up', top: b.l, bot: a.h, i });
      if (b.h < a.l && a.l - b.h >= fvgMinAtr * atr) fvgs.push({ dir: 'down', top: a.l, bot: b.h, i });
    }
  }

  const last = events[events.length - 1] || null;
  return { trend, bias: last?.dir || null, last, events, atr, lastBar: bars[bars.length - 1]?.t ?? null };
}

// ¿la estructura permite esta direccion? mode: 'bias' (ultimo evento) | 'trend' (ultima ruptura) | 'both' (cualquiera en contra bloquea)
export function allows(state, side, mode = 'bias') {
  if (!state) return { ok: true };
  const against = side === 'short' ? 'up' : 'down';
  const by = [];
  if ((mode === 'bias' || mode === 'both') && state.bias === against) by.push(`${state.last.type} ${against}`);
  if ((mode === 'trend' || mode === 'both') && state.trend === against) by.push(`tendencia ${against}`);
  return by.length ? { ok: false, why: by.join(' + '), at: state.last?.t } : { ok: true };
}
