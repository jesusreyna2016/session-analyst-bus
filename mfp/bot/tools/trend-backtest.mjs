// Prueba los filtros de tendencia (src/structure.mjs + EMAs + VWAP/TWAP) sobre el historico de zonas
// (zones/backtest/events.jsonl, R de orden limite en la entrada) con las velas de 5m de futuros de bars/.
// node mfp/bot/tools/trend-backtest.mjs   (OUT=archivo.json guarda cada trade con sus filtros)
import fs from 'fs';
import { analyze, allows } from '../src/structure.mjs';
import { fileURLToPath } from 'url';
const ROOT=fileURLToPath(new URL('../../../', import.meta.url)).replace(/\/$/,'');
const bars={};
for (const f of fs.readdirSync(ROOT+'/bars').sort()) {
  const d=JSON.parse(fs.readFileSync(`${ROOT}/bars/${f}`));
  for (const [s,arr] of Object.entries(d.symbols||{})) { (bars[s] ||= new Map()); for (const [t,o,h,l,c] of arr) bars[s].set(t*1000,{t:t*1000,o,h,l,c}); }
}
for (const s in bars) bars[s]=[...bars[s].values()].sort((a,b)=>a.t-b.t);
const ev=fs.readFileSync(ROOT+'/zones/backtest/events.jsonl','utf8').trim().split('\n').map(JSON.parse);
// emparejar: resolucion con rl <- ultima 'tocada' del mismo sym|id antes de ella
const lastTouch=new Map(); const trades=[];
for (const e of ev.sort((a,b)=>a.t-b.t)) {
  const k=e.sym+'|'+e.id+'|'+e.side;
  if (e.ev==='tocada') { if(!lastTouch.has(k)) lastTouch.set(k,e); }
  else if ((e.ev==='funciono'||e.ev==='invalidada') && e.f?.rl!=null) { const tt=lastTouch.get(k); lastTouch.delete(k); if (tt) trades.push({sym:e.sym,side:e.side,grade:e.grade,T:tt.t,R:e.f.rl,res:e.ev}); }
}
const idx=(arr,T)=>{let lo=0,hi=arr.length;while(lo<hi){const m=(lo+hi)>>1; if(arr[m].t<T) lo=m+1; else hi=m;} return lo;};
const agg=(b5,n)=>{const out=[];for(const b of b5){const k=Math.floor(b.t/(n*300000))*n*300000;const l=out[out.length-1]; if(l&&l.t===k){l.h=Math.max(l.h,b.h);l.l=Math.min(l.l,b.l);l.c=b.c;l.cnt++;} else out.push({t:k,o:b.o,h:b.h,l:b.l,c:b.c,cnt:1});} return out.filter(x=>x.cnt===n);};
const ema=(a,n)=>{let e=null;const k=2/(n+1);for(const x of a) e=e==null?x:e+(x-e)*k;return e;};
const ctHour=(t)=>+new Intl.DateTimeFormat('en-US',{timeZone:'America/Chicago',hour:'numeric',hour12:false}).format(new Date(t));
const sessStart=(t)=>{ // 17:00 CT mas reciente
  let s=Math.floor(t/3600000)*3600000; for(let i=0;i<30;i++){ if(ctHour(s)===17) return s; s-=3600000;} return t-86400000; };
const rows=[];
for (const tr of trades) {
  const B=bars[tr.sym]; if(!B) continue;
  const i=idx(B,tr.T-300000); // velas que cerraron antes de la vela del toque
  if(i<400) continue;
  const w=B.slice(i-600<0?0:i-600,i);
  const last=w[w.length-1]; if(tr.T-last.t>3600000) continue;
  const s5=analyze(w), s15=analyze(agg(w,3));
  const ss=sessStart(tr.T); const sesB=w.filter(b=>b.t>=ss); const twap=sesB.length?sesB.reduce((a,b)=>a+(b.h+b.l+b.c)/3,0)/sesB.length:null;
  const C=w.map(b=>b.c); const C15=agg(w,3).map(b=>b.c);
  const f={
    s5bias:allows(s5,tr.side,'bias').ok, s5trend:allows(s5,tr.side,'trend').ok,
    s15bias:allows(s15,tr.side,'bias').ok, s15trend:allows(s15,tr.side,'trend').ok,
  };
  const dn=tr.side==='short';
  if (twap!=null) f.vwapWith = dn ? last.c<twap : last.c>twap;
  f.ema9_21 = dn ? ema(C,9)<ema(C,21) : ema(C,9)>ema(C,21);
  f.ema20_50 = dn ? ema(C,20)<ema(C,50) : ema(C,20)>ema(C,50);
  f.ema200 = dn ? last.c<ema(C,200) : last.c>ema(C,200);
  f.ema15_20_50 = dn ? ema(C15,20)<ema(C15,50) : ema(C15,20)>ema(C15,50);
  rows.push({...tr,f,month:new Date(tr.T).toISOString().slice(0,7)});
}
fs.writeFileSync('/tmp/claude-0/-home-user/2f32d3d5-7671-5862-97d0-a1a3664d8808/scratchpad/hist_rows.json',JSON.stringify(rows));
const st=(a)=>{const n=a.length;const s=a.reduce((x,y)=>x+y.R,0);const w=a.filter(x=>x.R>0).length;return n?`n=${String(n).padStart(4)} avg=${(s/n).toFixed(3).padStart(6)}R tot=${s.toFixed(1).padStart(7)}R win=${(100*w/n).toFixed(0)}%`:'n=0';};
for (const grades of [['A+','A'],['A+','A','B']]) {
  const R=rows.filter(r=>grades.includes(r.grade));
  console.log(`\n### grados ${grades.join(',')}  TODAS: ${st(R)}`);
  const H1=R.filter(r=>r.T<Date.parse('2026-10-01')), H2=R.filter(r=>r.T>=Date.parse('2026-10-01'));
  for (const k of Object.keys(R[0].f)) {
    const p=R.filter(r=>r.f[k]===true), b=R.filter(r=>r.f[k]===false);
    console.log(`${k.padEnd(12)} PASA ${st(p)} | BLOQ ${st(b)} | sep ${st(H1.filter(r=>r.f[k]))} | oct+ ${st(H2.filter(r=>r.f[k]))}`);
  }
}
