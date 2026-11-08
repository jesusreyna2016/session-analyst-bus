#!/usr/bin/env python3
"""Agente de aprendizaje de zonas de Mi Mesa: analisis (solo libreria estandar).

Lee   zones/events/*.jsonl, zones/trades.json, zones/weights.json, zones/experiments.json
Escribe zones/report.json, zones/report.md, zones/state.json y actualiza 'verdict' en experiments.json.

Unidad de analisis = una zona de un dia (sym + id + dia CT). Un SETUP es una zona que se ARMO (despues del
toque, una vela de 5 min cerro de vuelta: es la entrada). Su resultado:
  funciono   -> gana, R = rr (distancia a TP1 en R)
  invalidada -> pierde, R = -1
  sin evento -> abierta (no cuenta para el acierto)
Ademas se mide la zona TOCADA que nunca se armo (para saber si el gatillo ayuda) y se cruzan los trades
reales de Jesus con las zonas (con ficha o por precio/hora).

Uso: python3 zones/analyze_zones.py [--days N]   (N = ventana reciente, por defecto 14)
"""
import json, math, os, sys, glob, datetime
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_N = 20          # muestra minima para sacar conclusiones de un segmento
EXP_MIN = 30        # muestra minima por politica para cerrar un experimento
FAM_SYM = {'NQ': 'NQ', 'ES': 'ES', 'GC': 'GC', 'YM': 'YM', 'CL': 'CL', 'ETH': 'ETHUSDT', 'BTC': 'BTCUSDT',
           'MNQ': 'NQ', 'MES': 'ES', 'MGC': 'GC', 'MYM': 'YM', 'MCL': 'CL'}
GRADES = ['A+', 'A', 'B']
RANK = {'A+': 3, 'A': 2, 'B': 1, 'C': 0}


def load_json(path, default):
    try:
        with open(path) as fh:
            return json.load(fh)
    except Exception:
        return default


def wilson(w, n, z=1.96):
    if n == 0:
        return (None, None)
    p = w / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - m) / d, 3), round((c + m) / d, 3))


def stats(rows):
    """rows: setups resueltos con 'win' y 'R'."""
    n = len(rows)
    w = sum(1 for r in rows if r['win'])
    rs = [r['R'] for r in rows if r['R'] is not None]
    gain = sum(x for x in rs if x > 0)
    loss = -sum(x for x in rs if x < 0)
    lo, hi = wilson(w, n)
    return {
        'n': n, 'wins': w, 'wr': round(w / n, 3) if n else None, 'wrLo': lo, 'wrHi': hi,
        'eR': round(sum(rs) / len(rs), 3) if rs else None,
        'pf': round(gain / loss, 2) if loss > 0 else (None if not gain else 99.0),
        'enough': n >= MIN_N,
    }


def bucket(v, edges, labels):
    if v is None:
        return 'sin dato'
    for e, l in zip(edges, labels):
        if v < e:
            return l
    return labels[-1]


# ------------------------------------------------------------------ zonas
def load_events():
    evs = []
    for path in sorted(glob.glob(os.path.join(HERE, 'events', '*.jsonl'))):
        day = os.path.basename(path)[:10]
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                e['day'] = day
                evs.append(e)
    return evs


def build_zones(evs):
    zones = {}
    for e in sorted(evs, key=lambda x: x.get('t') or 0):
        k = (e['day'], e.get('sym'), e.get('id'))
        z = zones.setdefault(k, {'day': e['day'], 'sym': e.get('sym'), 'id': e.get('id'), 'side': e.get('side'),
                                 'lo': e.get('lo'), 'hi': e.get('hi'), 'grade': e.get('grade'), 'f': {}, 'ev': {}})
        z['ev'][e.get('ev')] = e.get('t')
        f = e.get('f') or {}
        # el contexto del primer evento manda (como estaba la zona cuando aparecio / se toco); mfe/mae al final
        for kk, vv in f.items():
            if kk in ('mfe', 'mae') or kk not in z['f']:
                z['f'][kk] = vv
        if e.get('ev') in ('tocada', 'armada'):
            z['grade'] = e.get('grade') or z['grade']
        for kk in ('entry', 'stop', 'tp1'):
            if e.get(kk) is not None:
                z[kk] = e.get(kk)
    out = []
    for z in zones.values():
        ev = z['ev']
        f = z['f']
        z['armed'] = 'armada' in ev
        z['touched'] = 'tocada' in ev or z['armed']
        res = 'win' if 'funciono' in ev else 'loss' if 'invalidada' in ev else None
        z['result'] = res
        rr = f.get('rr')
        z['R'] = (rr if rr is not None else 1.0) if res == 'win' else (-1.0 if res == 'loss' else None)
        z['win'] = res == 'win'
        out.append(z)
    return out


def seg_table(setups, keyfn):
    groups = defaultdict(list)
    for s in setups:
        groups[keyfn(s)].append(s)
    return {k: stats(v) for k, v in sorted(groups.items(), key=lambda kv: str(kv[0]))}


def key_lift(setups):
    """Para cada nivel/confluencia: acierto con y sin ella (que confluencia gana mas)."""
    allk = set()
    for s in setups:
        allk.update(k for k in (s['f'].get('keys') or '').split('+') if k)
    out = {}
    for k in sorted(allk):
        with_k = [s for s in setups if k in (s['f'].get('keys') or '').split('+')]
        wo = [s for s in setups if k not in (s['f'].get('keys') or '').split('+')]
        a, b = stats(with_k), stats(wo)
        out[k] = {'with': a, 'without': b,
                  'lift': round(a['wr'] - b['wr'], 3) if a['wr'] is not None and b['wr'] is not None else None}
    return out


def policy(setups, gradefield, min_grade):
    rows = [s for s in setups if RANK.get(s.get(gradefield) if gradefield == 'grade' else s['f'].get('gradeS'), 0) >= RANK[min_grade]]
    return stats(rows)


# ------------------------------------------------------------------ trades
def match_trades(trades, zones):
    by_day_sym = defaultdict(list)
    for z in zones:
        by_day_sym[(z['day'], z['sym'])].append(z)
    rows = []
    for t in trades:
        sym = FAM_SYM.get((t.get('fam') or '').upper(), (t.get('fam') or '').upper())
        cands = by_day_sym.get((t.get('day'), sym), [])
        entry, side, t0 = t.get('entry'), t.get('side'), t.get('topen') or 0
        zone, how = None, None
        if t.get('zoneId'):
            for z in cands:
                if z['id'] == t['zoneId'] or (z['side'] == side and t.get('zoneLo') is not None and z['lo'] is not None
                                              and t['zoneLo'] <= z['hi'] and z['lo'] <= (t.get('zoneHi') or t['zoneLo'])):
                    zone, how = z, 'ficha'
                    break
            if zone is None:
                how = 'ficha (zona sin datos del indicador)'
        if zone is None and entry is not None:
            for z in cands:
                if z['side'] != side or z['lo'] is None:
                    continue
                pad = (z['hi'] - z['lo']) * 0.5
                born = min(v for v in z['ev'].values() if v) if z['ev'] else 0
                if z['lo'] - pad <= entry <= z['hi'] + pad and born <= t0:
                    zone, how = z, 'precio'
                    break
        # cruce automatico del servidor (zone-trades): tambien usa el registro del plan del servidor, asi cubre
        # zonas que el indicador no reporto (grafico cerrado, sin webhook)
        auto = t.get('auto') or None
        armed_at = zone['ev'].get('armada') if zone else None
        if zone is None and auto:
            how = 'auto (' + (auto.get('src') or 'servidor') + ')'
            armed_at = auto.get('armedAt')
        rows.append({
            'id': t.get('id'), 'day': t.get('day'), 'sym': sym, 'side': side, 'R': t.get('R'),
            'inZone': zone is not None or bool(t.get('zoneId')) or bool(auto), 'how': how or 'fuera de zona',
            'zoneGrade': (zone or {}).get('grade') or t.get('zoneGrade') or (auto or {}).get('grade'), 'zoneResult': (zone or {}).get('result'),
            'zoneR': (zone or {}).get('R'), 'beforeTrigger': (t0 < armed_at) if (armed_at and t0) else None,
            'noTrigger': bool(zone and not zone['armed']) or bool(zone is None and auto and not auto.get('armed')), 'hasPlan': t.get('hasPlan'), 'followed': t.get('followed'),
            'againstBias': t.get('againstBias'), 'session': t.get('session'),
        })
    return rows


def rstats(rows):
    rs = [r['R'] for r in rows if r.get('R') is not None]
    n = len(rs)
    w = sum(1 for x in rs if x > 0)
    gain = sum(x for x in rs if x > 0)
    loss = -sum(x for x in rs if x < 0)
    return {'n': n, 'wr': round(w / n, 3) if n else None, 'eR': round(sum(rs) / n, 3) if n else None,
            'totalR': round(sum(rs), 2) if n else 0, 'pf': round(gain / loss, 2) if loss > 0 else None}


def segments(setups):
    f = lambda s, k: s['f'].get(k)
    al = lambda s: {'1': 'a favor', '0': 'neutral', '-1': 'contra'}.get(str(f(s, 'al')), 'sin dato')
    return {
        'grado': seg_table(setups, lambda s: s.get('grade') or '?'),
        'mercado': seg_table(setups, lambda s: s['sym']),
        'lado': seg_table(setups, lambda s: s['side']),
        'direccion': seg_table(setups, al),
        'regimen': seg_table(setups, lambda s: f(s, 'reg') or 'sin dato'),
        'sesion': seg_table(setups, lambda s: f(s, 'sess') or 'sin dato'),
        'grado x regimen': seg_table(setups, lambda s: (s.get('grade') or '?') + ' · ' + (f(s, 'reg') or 'sin dato')),
        'grado x direccion': seg_table(setups, lambda s: (s.get('grade') or '?') + ' · ' + al(s)),
        'grado x mercado': seg_table(setups, lambda s: (s.get('grade') or '?') + ' · ' + s['sym']),
        'chop': seg_table(setups, lambda s: bucket(f(s, 'chop'), [50, 61.8], ['<50 tendencia', '50-61.8', '>=61.8 lateral'])),
        'estirado (ATR del VWAP)': seg_table(setups, lambda s: bucket(f(s, 'str'), [1, 2], ['<1', '1-2', '>=2'])),
        'R hasta TP1': seg_table(setups, lambda s: bucket(f(s, 'rr'), [1.5, 2.5], ['<1.5R', '1.5-2.5R', '>=2.5R'])),
        'distancia al crearse (ATR)': seg_table(setups, lambda s: bucket(f(s, 'dist'), [2, 6], ['<2', '2-6', '>=6'])),
    }


def excursion_of(setups):
    f = lambda s, k: s['f'].get(k)
    mfe_losers = [f(s, 'mfe') for s in setups if not s['win'] and f(s, 'mfe') is not None]
    mae_winners = [f(s, 'mae') for s in setups if s['win'] and f(s, 'mae') is not None]
    return {
        'losersMfeAvgR': round(sum(mfe_losers) / len(mfe_losers), 2) if mfe_losers else None,
        'losersThatReached1R': sum(1 for x in mfe_losers if x >= 1),
        'losersN': len(mfe_losers),
        'winnersMaeAvgR': round(sum(mae_winners) / len(mae_winners), 2) if mae_winners else None,
        'winnersN': len(mae_winners),
    }


# ------------------------------------------------------------------ historico (backtest)
def chicago_day(ms):
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.fromtimestamp(ms / 1000, ZoneInfo('America/Chicago')).strftime('%Y-%m-%d')
    except Exception:
        return datetime.datetime.fromtimestamp(ms / 1000 - 6 * 3600, datetime.timezone.utc).strftime('%Y-%m-%d')


def backtest_section():
    """zones/backtest/events.jsonl (backtest.mjs): el mismo motor sobre las velas del bus. R real = entrar al cierre
    de la vela del gatillo y salir en TP1 o al cierre que invalida (rx); el R 'teorico' usa la entrada de la zona."""
    path = os.path.join(HERE, 'backtest', 'events.jsonl')
    if not os.path.exists(path):
        return None
    evs = []
    with open(path) as fh:
        for line in fh:
            try:
                e = json.loads(line)
            except Exception:
                continue
            e['day'] = chicago_day(e.get('t') or 0)
            evs.append(e)
    zones = build_zones(evs)
    armed = [z for z in zones if z['armed']]
    setups = [z for z in armed if z['result']]
    theo = stats(setups)
    for z in setups:
        if z['f'].get('rx') is not None:
            z['R'] = z['f']['rx']
    touched_only = [z for z in zones if z['touched'] and not z['armed'] and z['result']]
    # como entrar: gatillo (cierre de la vela de 5 min) vs orden limite en la entrada de la zona, sobre las zonas tocadas
    def entry_stats(rows, key):
        rr = [dict(z, R=z['f'][key], win=z['f'][key] > 0) for z in rows if z['f'].get(key) is not None]
        return stats(rr)
    resolved_touched = [z for z in zones if z['touched'] and z['result']]
    entries = {
        'gatillo (cierre de la vela de 5 min)': entry_stats(resolved_touched, 'rx'),
        'limite en la entrada, todas las tocadas': entry_stats(resolved_touched, 'rl'),
        'limite en la entrada, solo las que se armaron': entry_stats([z for z in resolved_touched if z['armed']], 'rl'),
        'limite en la entrada, las que NUNCA se armaron': entry_stats([z for z in resolved_touched if not z['armed']], 'rl'),
        'gatillo y luego limite si regresa a la entrada': entry_stats([z for z in resolved_touched if z['armed']], 'rp'),
    }
    armed_res = [z for z in resolved_touched if z['armed']]
    pb_n = sum(1 for z in armed_res if z['f'].get('rp') is not None)
    entries_note = {'pullbackFillRate': round(pb_n / len(armed_res), 3) if armed_res else None, 'armedResolved': len(armed_res)}
    entries_by_grade = {g: {'gatillo': entry_stats([z for z in resolved_touched if z.get('grade') == g], 'rx'),
                            'limite': entry_stats([z for z in resolved_touched if z.get('grade') == g], 'rl')} for g in GRADES}
    meta = load_json(os.path.join(HERE, 'backtest', 'summary.json'), {})
    days = sorted({z['day'] for z in zones})
    return {
        'generatedAt': meta.get('generatedAt'), 'notes': meta.get('notes'),
        'counts': {'zones': len(zones), 'armed': len(armed), 'resolved': len(setups), 'days': len(days),
                   'from': days[0] if days else None, 'to': days[-1] if days else None},
        'overallTheoretical': theo, 'overall': stats(setups),
        'segments': segments(setups), 'confluence': key_lift(setups), 'excursion': excursion_of(setups),
        'trigger': {'armadas': stats(setups), 'tocadasSinGatillo': stats(touched_only)},
        'entries': entries, 'entriesByGrade': entries_by_grade, 'entriesNote': entries_note,
    }


# ------------------------------------------------------------------ main
def main():
    days_recent = 14
    if '--days' in sys.argv:
        days_recent = int(sys.argv[sys.argv.index('--days') + 1])
    today = datetime.date.today()
    since = (today - datetime.timedelta(days=days_recent)).isoformat()

    evs = load_events()
    zones = build_zones(evs)
    weights = load_json(os.path.join(HERE, 'weights.json'), {})
    exps = load_json(os.path.join(HERE, 'experiments.json'), {'experiments': []})
    trades = list((load_json(os.path.join(HERE, 'trades.json'), {}).get('trades') or {}).values())

    armed = [z for z in zones if z['armed']]
    setups = [z for z in armed if z['result']]
    recent = [z for z in setups if z['day'] >= since]
    touched_only = [z for z in zones if z['touched'] and not z['armed'] and z['result']]
    f = lambda s, k: s['f'].get(k)

    seg = segments(setups)
    excursion = excursion_of(setups)  # MFE/MAE: si TP1 es corto o el stop es apretado
    trigger = {'armadas': stats(setups), 'tocadasSinGatillo': stats(touched_only)}

    # politicas: pesos activos vs en prueba (sombra)
    has_shadow = any(s['f'].get('gradeS') for s in setups)
    policies = {}
    for g in GRADES:
        policies[g] = {'active': policy(setups, 'grade', g), 'shadow': policy(setups, 'gradeS', g) if has_shadow else None}

    # experimentos en sombra: compara desde su startDate
    for ex in exps.get('experiments', []):
        if ex.get('status') != 'shadow' or not ex.get('startDate'):
            continue
        rows = [s for s in setups if s['day'] >= ex['startDate'] and s['f'].get('wsv') == ex.get('shadowVersion')]
        g = ex.get('minGrade', 'A')
        a, b = policy(rows, 'grade', g), policy(rows, 'gradeS', g)
        ex['eval'] = {'asOf': today.isoformat(), 'minGrade': g, 'active': a, 'shadow': b}
        if a['n'] >= EXP_MIN and b['n'] >= EXP_MIN and a['eR'] is not None and b['eR'] is not None:
            better = b['eR'] - a['eR']
            ex['verdict'] = 'mejora' if better >= 0.1 else 'empeora' if better <= -0.1 else 'igual'
        else:
            ex['verdict'] = 'muestra corta'

    # trades reales
    trows = match_trades(trades, zones)
    tr = {
        'todos': rstats(trows),
        'en zona': rstats([r for r in trows if r['inZone']]),
        'fuera de zona': rstats([r for r in trows if not r['inZone']]),
        'en zona con ficha': rstats([r for r in trows if r['how'] == 'ficha']),
        'en zona sin ficha (por precio)': rstats([r for r in trows if r['how'] == 'precio']),
        'antes del gatillo': rstats([r for r in trows if r['beforeTrigger']]),
        'despues del gatillo': rstats([r for r in trows if r['beforeTrigger'] is False]),
        'zona que nunca se armo': rstats([r for r in trows if r['noTrigger']]),
    }
    by_grade_user = {g: rstats([r for r in trows if r['zoneGrade'] == g]) for g in GRADES}
    gap = [r for r in trows if r['zoneResult'] and r['R'] is not None]
    execution = {
        'zonaGanoTuPerdiste': sum(1 for r in gap if r['zoneResult'] == 'win' and r['R'] < 0),
        'zonaPerdioTuGanaste': sum(1 for r in gap if r['zoneResult'] == 'loss' and r['R'] > 0),
        'n': len(gap),
        'tuRvsZonaR': round(sum(r['R'] - (r['zoneR'] or 0) for r in gap) / len(gap), 2) if gap else None,
    }

    def flat(z):
        return {'day': z['day'], 'sym': z['sym'], 'id': z['id'], 'side': z['side'], 'grade': z.get('grade'),
                'result': z['result'], 'R': z['R'], **{k: z['f'].get(k) for k in ('gradeS', 'al', 'reg', 'sess', 'rr', 'chop', 'str', 'keys', 'mfe', 'mae')}}

    report = {
        'generatedAt': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, tzinfo=None).isoformat() + 'Z',
        'weightsVersion': weights.get('version'), 'shadowVersion': weights.get('shadowVersion'),
        'counts': {'events': len(evs), 'zones': len(zones), 'armed': len(armed), 'resolved': len(setups),
                   'open': len(armed) - len(setups), 'days': len({z['day'] for z in zones}), 'trades': len(trades)},
        'overall': stats(setups), 'recent': {'since': since, **stats(recent)},
        'segments': seg, 'confluence': key_lift(setups), 'trigger': trigger, 'excursion': excursion,
        'policies': policies, 'experiments': exps.get('experiments', []),
        'trades': tr, 'tradesByZoneGrade': by_grade_user, 'execution': execution,
        'setups': [flat(z) for z in setups[-400:]],
        'backtest': backtest_section(),
    }
    with open(os.path.join(HERE, 'report.json'), 'w') as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, 'experiments.json'), 'w') as fh:
        json.dump(exps, fh, indent=2, ensure_ascii=False)

    # resumen corto para Mi Mesa
    state = {
        'generatedAt': report['generatedAt'], 'weightsVersion': weights.get('version'),
        'shadowVersion': weights.get('shadowVersion'), 'counts': report['counts'],
        'byGrade': {g: seg['grado'].get(g) for g in GRADES if seg['grado'].get(g)},
        'recent': report['recent'], 'trades': {k: tr[k] for k in ('en zona', 'fuera de zona', 'antes del gatillo', 'despues del gatillo')},
        'execution': execution,
        'experiments': [{k: e.get(k) for k in ('id', 'status', 'hypothesis', 'verdict', 'startDate')} for e in exps.get('experiments', [])][-5:],
        'insights': load_json(os.path.join(HERE, 'state.json'), {}).get('insights', []),
        'backtest': ({'counts': report['backtest']['counts'], 'overall': report['backtest']['overall'],
                      'byGrade': {g: report['backtest']['segments']['grado'].get(g) for g in GRADES if report['backtest']['segments']['grado'].get(g)},
                      'noTrigger': report['backtest']['trigger']['tocadasSinGatillo'],
                      'entries': {'gatillo': report['backtest']['entries']['gatillo (cierre de la vela de 5 min)'],
                                  'limite': report['backtest']['entries']['limite en la entrada, todas las tocadas']}} if report.get('backtest') else None),
    }
    with open(os.path.join(HERE, 'state.json'), 'w') as fh:
        json.dump(state, fh, indent=1, ensure_ascii=False)

    write_md(report)
    print(f"zonas {len(zones)} · armadas {len(armed)} · resueltas {len(setups)} · trades {len(trades)} -> report.md")


def pct(x):
    return '–' if x is None else f"{round(x * 100)}%"


def row(name, s):
    if not s or not s.get('n'):
        return f"| {name} | 0 | – | – | – |"
    ci = f"{pct(s['wrLo'])}–{pct(s['wrHi'])}" if s.get('wrLo') is not None else '–'
    flag = '' if s.get('enough', True) else ' ·'
    return f"| {name} | {s['n']}{flag} | {pct(s['wr'])} ({ci}) | {s['eR'] if s['eR'] is not None else '–'} | {s.get('pf') or '–'} |"


def write_md(r):
    L = []
    c = r['counts']
    L.append(f"# Zonas de Mi Mesa · reporte del agente\n")
    L.append(f"Generado {r['generatedAt']} · pesos `{r['weightsVersion']}`" + (f" · en prueba `{r['shadowVersion']}`" if r['shadowVersion'] else ''))
    L.append(f"\n{c['days']} dias · {c['zones']} zonas · {c['armed']} armadas ({c['resolved']} resueltas, {c['open']} abiertas) · {c['trades']} trades de Mi Mesa.")
    L.append(f"\n`·` = muestra menor a {MIN_N}: no sacar conclusiones. Acierto con intervalo 95% (Wilson). E[R] = R promedio por setup.\n")
    L.append("## Setups armados (gatillo de 5 min)\n")
    L.append("| | n | acierto | E[R] | PF |\n|---|---|---|---|---|")
    L.append(row('Todos', r['overall']))
    L.append(row(f"Ultimos dias (desde {r['recent']['since']})", r['recent']))
    L.append(row('Tocadas que NUNCA se armaron', r['trigger']['tocadasSinGatillo']))
    for name, tab in r['segments'].items():
        L.append(f"\n### Por {name}\n\n| | n | acierto | E[R] | PF |\n|---|---|---|---|---|")
        for k, s in tab.items():
            L.append(row(k, s))
    L.append("\n## Confluencias: acierto con y sin cada nivel\n\n| nivel | n con | acierto con | acierto sin | diferencia |\n|---|---|---|---|---|")
    for k, v in sorted(r['confluence'].items(), key=lambda kv: -(kv[1]['lift'] or -9)):
        L.append(f"| {k} | {v['with']['n']} | {pct(v['with']['wr'])} | {pct(v['without']['wr'])} | {'–' if v['lift'] is None else ('+' if v['lift'] > 0 else '') + str(round(v['lift'] * 100)) + ' pts'} |")
    e = r['excursion']
    L.append(f"\n## Excursion\n\nPerdedoras: se movieron a favor {e['losersMfeAvgR']}R en promedio; {e['losersThatReached1R']} de {e['losersN']} llegaron a +1R antes del stop. Ganadoras: en contra {e['winnersMaeAvgR']}R en promedio (n {e['winnersN']}).")
    L.append("\n## Pesos activos vs en prueba (politica: tomar desde la calificacion)\n\n| desde | activos n | activos acierto | activos E[R] | prueba n | prueba acierto | prueba E[R] |\n|---|---|---|---|---|---|---|")
    for g, p in r['policies'].items():
        a, b = p['active'], p['shadow'] or {}
        L.append(f"| {g} | {a['n']} | {pct(a['wr'])} | {a['eR']} | {b.get('n', '–')} | {pct(b.get('wr'))} | {b.get('eR', '–')} |")
    L.append("\n## Experimentos\n")
    if not r['experiments']:
        L.append("Ninguno todavia.")
    for ex in r['experiments']:
        L.append(f"- **{ex.get('id')}** ({ex.get('status')}): {ex.get('hypothesis')} · veredicto: {ex.get('verdict', '–')}")
    L.append("\n## Tus trades contra las zonas\n\n| | n | acierto | E[R] | R total | PF |\n|---|---|---|---|---|---|")
    for k, s in r['trades'].items():
        L.append(f"| {k} | {s['n']} | {pct(s['wr'])} | {s['eR'] if s['eR'] is not None else '–'} | {s['totalR']} | {s['pf'] or '–'} |")
    L.append("\n| zona del trade | n | acierto | E[R] |\n|---|---|---|---|")
    for g, s in r['tradesByZoneGrade'].items():
        L.append(f"| {g} | {s['n']} | {pct(s['wr'])} | {s['eR'] if s['eR'] is not None else '–'} |")
    x = r['execution']
    L.append(f"\nEjecucion ({x['n']} trades con zona resuelta): la zona gano y tu perdiste {x['zonaGanoTuPerdiste']} veces; la zona perdio y tu ganaste {x['zonaPerdioTuGanaste']}. Tu R menos el R de la zona, en promedio: {x['tuRvsZonaR']}.")
    bt = r.get('backtest')
    if bt:
        bc = bt['counts']
        L.append(f"\n## Historico (backtest)\n\nEl mismo motor sobre las velas de 5 min del bus, {bc['from']} a {bc['to']} ({bc['days']} dias): {bc['zones']} zonas tocadas, {bc['armed']} armadas, {bc['resolved']} resueltas. {bt.get('notes') or ''}.")
        L.append("E[R] **real**: entrando al cierre de la vela del gatillo y saliendo en TP1 o al cierre que invalida. Sirve para proponer experimentos; el vivo es el que confirma.\n")
        L.append("| | n | acierto | E[R] | PF |\n|---|---|---|---|---|")
        L.append(row('Todos (R real)', bt['overall']))
        L.append(row('Todos (R teorico, entrada de la zona)', bt['overallTheoretical']))
        L.append(row('Tocadas que NUNCA se armaron', bt['trigger']['tocadasSinGatillo']))
        L.append("\n### Historico: como entrar (R real)\n\n| | n | acierto | E[R] | PF |\n|---|---|---|---|---|")
        for k, s2 in bt['entries'].items():
            L.append(row(k, s2))
        en = bt.get('entriesNote') or {}
        if en.get('pullbackFillRate') is not None:
            L.append(f"\nGatillo + regreso a la entrada: el precio volvio a la entrada en {pct(en['pullbackFillRate'])} de las {en['armedResolved']} armadas (las demas se pierden: no hay trade).")
        L.append("\n| grado | gatillo n | gatillo E[R] | limite n | limite acierto | limite E[R] |\n|---|---|---|---|---|---|")
        for g, d in bt['entriesByGrade'].items():
            L.append(f"| {g} | {d['gatillo']['n']} | {d['gatillo']['eR']} | {d['limite']['n']} | {pct(d['limite']['wr'])} | {d['limite']['eR']} |")
        for name, tab in bt['segments'].items():
            L.append(f"\n### Historico por {name}\n\n| | n | acierto | E[R] | PF |\n|---|---|---|---|---|")
            for k, s2 in tab.items():
                L.append(row(k, s2))
        L.append("\n### Historico: confluencias\n\n| nivel | n con | acierto con | acierto sin | diferencia |\n|---|---|---|---|---|")
        for k, v in sorted(bt['confluence'].items(), key=lambda kv: -(kv[1]['lift'] or -9)):
            L.append(f"| {k} | {v['with']['n']} | {pct(v['with']['wr'])} | {pct(v['without']['wr'])} | {'–' if v['lift'] is None else ('+' if v['lift'] > 0 else '') + str(round(v['lift'] * 100)) + ' pts'} |")
        e2 = bt['excursion']
        L.append(f"\nExcursion historica: perdedoras a favor {e2['losersMfeAvgR']}R en promedio, {e2['losersThatReached1R']} de {e2['losersN']} llegaron a +1R antes del stop; ganadoras en contra {e2['winnersMaeAvgR']}R (n {e2['winnersN']}).")
    with open(os.path.join(HERE, 'report.md'), 'w') as fh:
        fh.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
