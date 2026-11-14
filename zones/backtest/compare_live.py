# Live vs backtest comparison with the SAME R definition (theoretical: zone entry, +rr on win, -1 on loss).
# Usage: python -I zones/backtest/compare_live.py zones zones/backtest/live_vs_backtest.json
# Also writes histReal (rx: entry at trigger-bar close).
import sys, os, json
Z = sys.argv[1]
sys.path.insert(0, Z)
import analyze_zones as A
def keys(z): return set(str(z['f'].get('keys') or '').split('+'))
def segs(setups, touched_only):
    f = lambda s, k: s['f'].get(k)
    out = {
      'todos': A.stats(setups),
      'tocadas sin gatillo': A.stats(touched_only),
      'grado': A.seg_table(setups, lambda s: s.get('grade') or '?'),
      'estirado': A.seg_table(setups, lambda s: A.bucket(f(s,'str'), [1,2], ['<1','1-2','>=2'])),
      'f15m': A.seg_table(setups, lambda s: 'con f15m' if 'f15m' in keys(s) else 'sin f15m'),
      'NQ grado': A.seg_table([s for s in setups if s['sym']=='NQ'], lambda s: s.get('grade') or '?'),
    }
    return out
# vivo
evs = A.load_events(); zs = A.build_zones(evs)
live_set = [z for z in zs if z['armed'] and z['result']]
live_to = [z for z in zs if z['touched'] and not z['armed'] and z['result']]
# historico, R teorico (misma definicion que el vivo)
evs = []
for line in open(os.path.join(Z,'backtest','events.jsonl')):
    try: e = json.loads(line)
    except Exception: continue
    e['day'] = A.chicago_day(e.get('t') or 0); evs.append(e)
hz = A.build_zones(evs)
h_set = [z for z in hz if z['armed'] and z['result']]
h_to = [z for z in hz if z['touched'] and not z['armed'] and z['result']]
H = segs(h_set, h_to); L = segs(live_set, live_to)
# R real del historico
for z in h_set:
    if z['f'].get('rx') is not None: z['R'] = z['f']['rx']
HR = segs(h_set, [])
json.dump({'live': L, 'histTheoretical': H, 'histReal': HR}, open(sys.argv[2],'w',encoding='utf8'), ensure_ascii=False, indent=1)
def flat(d, p=''):
    for k,v in d.items():
        if isinstance(v, dict) and 'n' not in v: yield from flat(v, p+k+' / ')
        else: yield p+k, v
hd = dict(flat(H)); hr = dict(flat(HR))
print('%-32s %18s %18s %8s %8s  flag' % ('segmento','vivo n wr [IC]','hist n wr [IC]','vivoER','histER'))
for k, l in flat(L):
    h = hd.get(k)
    if not h or not l['n']: print(k, 'falta', l, h); continue
    flag = ''
    if h['wr'] < l['wrLo'] or h['wr'] > l['wrHi']: flag += ' HIST fuera IC vivo'
    if l['wr'] < h['wrLo'] or l['wr'] > h['wrHi']: flag += ' VIVO fuera IC hist'
    print('%-32s %4d %3.0f%% [%2.0f-%2.0f] %5d %3.0f%% [%2.0f-%2.0f] %8s %8s %s real=%s%s' % (k, l['n'], l['wr']*100, l['wrLo']*100, l['wrHi']*100, h['n'], h['wr']*100, h['wrLo']*100, h['wrHi']*100, l['eR'], h['eR'], '' , hr.get(k,{}).get('eR'), flag))
