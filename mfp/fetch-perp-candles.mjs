import WebSocket from 'ws'; import {HttpsProxyAgent} from 'https-proxy-agent'; import fs from 'fs';
const pairs=[['binance','CLUSDT'],['hyperliquid','xyz:CL'],['binance','XAUUSDT'],['hyperliquid','xyz:SP500'],['ostium','SP500'],['hyperliquid','xyz:XYZ100'],['ostium','NDX'],['ostium','DJI']];
const START=Date.parse('2026-08-20T00:00:00Z');
const ws=new WebSocket('wss://api-stream.myfundedperpetuals.com/v1/market-data',{agent:new HttpsProxyAgent(process.env.HTTPS_PROXY),perMessageDeflate:true});
let id=0; const pend=new Map();
const req=(payload)=>new Promise((res,rej)=>{const i=++id;pend.set(i,{res,rej});ws.send(JSON.stringify({op:'req',id:i,method:'candles.history',payload}));});
ws.on('message',d=>{const f=JSON.parse(d);const p=pend.get(f.id);if(!p)return;pend.delete(f.id);f.op==='res'?p.res(f.result):p.rej(new Error(JSON.stringify(f.error)));});
ws.on('open',async()=>{const out={};
 for(const [provider,symbol] of pairs){const m=new Map();let end=Date.now();
  for(let k=0;k<40;k++){let r;try{r=await req({provider,symbol,interval:'5m',limit:1000,endTime:end});}catch(e){console.log(symbol,'ERR',e.message.slice(0,200));break;}
   if(!r.length)break; for(const c of r) if(c.isFinal) m.set(c.openTime,+c.close);
   const first=Math.min(...r.map(c=>c.openTime)); if(first<=START||first>=end)break; end=first-1;}
  out[provider+'|'+symbol]=[...m.entries()].sort((a,b)=>a[0]-b[0]); const ks=[...m.keys()];
  console.log(provider,symbol,m.size,ks.length?new Date(Math.min(...ks)).toISOString():'-');}
 fs.writeFileSync(process.argv[2]||'perp.json',JSON.stringify(out)); ws.close();});
ws.on('error',e=>{console.error(e.message);process.exit(1)});
