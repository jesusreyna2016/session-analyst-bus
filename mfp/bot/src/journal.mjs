// Bitacora JSONL por dia (UTC) en DATA_DIR, con copia opcional al bus de GitHub.
import fs from 'node:fs';
import path from 'node:path';
import { fetch } from './net.mjs';

export const dayUtc = (ms = Date.now()) => new Date(ms).toISOString().slice(0, 10);

export class Journal {
  constructor(cfg) {
    this.cfg = cfg;
    this.dir = cfg.dataDir;
    fs.mkdirSync(this.dir, { recursive: true });
    this.dirty = new Set();
  }

  file(day) { return path.join(this.dir, `${day}.jsonl`); }

  write(evt, data = {}) {
    const rec = { ts: new Date().toISOString(), evt, ...data };
    const day = dayUtc();
    fs.appendFileSync(this.file(day), JSON.stringify(rec) + '\n');
    this.dirty.add(day);
    const quiet = evt === 'basis_sample' || evt === 'skip';
    if (!quiet || process.env.VERBOSE === '1') console.log(`[${rec.ts}] ${evt}`, JSON.stringify(data));
    return rec;
  }

  read(day) {
    const f = this.file(day);
    if (!fs.existsSync(f)) return [];
    return fs.readFileSync(f, 'utf8').split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  }

  writeFile(name, content) {
    fs.writeFileSync(path.join(this.dir, name), content);
    this.dirty.add(name);
  }

  // Sube los archivos cambiados a GH_REPO/GH_DIR via la API de contenidos (si hay GH_TOKEN)
  async syncGithub() {
    const { token, repo, branch, dir } = this.cfg.gh;
    if (!token || !this.dirty.size) return;
    const items = [...this.dirty];
    this.dirty.clear();
    for (const it of items) {
      const name = it.includes('.') ? it : `${it}.jsonl`;
      const local = path.join(this.dir, name);
      if (!fs.existsSync(local)) continue;
      const api = `https://api.github.com/repos/${repo}/contents/${dir}/${name}`;
      const h = { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json', 'User-Agent': 'mfp-zone-bot' };
      try {
        const cur = await fetch(`${api}?ref=${branch}`, { headers: h });
        const sha = cur.ok ? (await cur.json()).sha : undefined;
        const body = { message: `mfp-bot: ${name}`, branch, content: fs.readFileSync(local).toString('base64'), ...(sha ? { sha } : {}) };
        const r = await fetch(api, { method: 'PUT', headers: { ...h, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        if (!r.ok) { this.dirty.add(it); console.log('github sync', name, r.status, (await r.text()).slice(0, 200)); }
      } catch (e) {
        this.dirty.add(it);
        console.log('github sync error', e.message);
      }
    }
  }
}
