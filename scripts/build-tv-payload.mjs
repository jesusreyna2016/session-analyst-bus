#!/usr/bin/env node
/**
 * CLI: plan JSON → Overlay v2 payload lines (one per SYM)
 * Usage: node scripts/build-tv-payload.mjs <plan.json> [--classic]
 */
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const SAPayload = require(join(__dirname, "../hud/tv-payload.js"));

const args = process.argv.slice(2);
if (!args.length || args.includes("-h") || args.includes("--help")) {
  console.error("Usage: node scripts/build-tv-payload.mjs <plan.json> [--classic]");
  process.exit(args.length ? 0 : 1);
}
const classicOnly = args.includes("--classic");
const file = args.find((a) => !a.startsWith("-"));
const plan = JSON.parse(readFileSync(file, "utf8"));
const all = SAPayload.buildAll(plan, { classicOnly });
for (const sym of Object.keys(all)) {
  console.log(`${sym}\t${all[sym]}`);
}
