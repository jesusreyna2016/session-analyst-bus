/**
 * SA Overlay v2 · shared payload builder
 * Works in browser (HUD) and Node (scripts/build-tv-payload.mjs).
 * Classic keys preserved; v2 adds VSCORE FCONFLICT WHIP DIR HYP PRED.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.SAPayload = factory();
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function L(x) {
    if (x == null) return "";
    if (typeof x === "object") return x.es || x.en || "";
    return String(x);
  }
  function saNum(x) {
    if (x == null || x === "") return null;
    var n = +x;
    return isNaN(n) ? null : n;
  }
  function saRange(a) {
    return Array.isArray(a) && a.length === 2 && a[0] != null && a[1] != null
      ? a[0] + "-" + a[1]
      : null;
  }
  function saGolden(d, az) {
    var r = null;
    if (d && d.scenarioB && saRange(d.scenarioB.zone)) r = saRange(d.scenarioB.zone);
    else {
      var t = d && d.scenarioB ? L(d.scenarioB.text) : "";
      var m = t && t.match(/(\d{3,6}(?:\.\d+)?)\s*[-–]\s*(\d{3,6}(?:\.\d+)?)/);
      if (m) r = m[1] + "-" + m[2];
    }
    return r && r !== az ? r : null;
  }
  function saT2(d, t1, bias) {
    var s = d && d.scenarioA;
    if (!s) return null;
    if (s.target2 != null && !isNaN(+s.target2)) return +s.target2;
    if (t1 == null) return null;
    var t = L(s.text) || "";
    var short = String(bias).toUpperCase() === "SHORT";
    var nums = (t.match(/\d{3,6}(?:\.\d+)?/g) || []).map(Number);
    for (var i = 0; i < nums.length; i++) {
      var n = nums[i];
      if (short ? n < t1 : n > t1) return n;
    }
    return null;
  }
  function saWin(z) {
    var w = z && z.play ? L(z.play.window) : "";
    var m = w && w.match(/(\d{1,2}):(\d{2})\s*[-–]\s*(\d{1,2}):(\d{2})/);
    if (!m) return null;
    var p = function (h) {
      h = +h;
      return (h < 10 ? "0" : "") + h;
    };
    return p(m[1]) + m[2] + "-" + p(m[3]) + m[4];
  }
  function saStop(z) {
    var t = z && z.play ? L(z.play.structStop) : "";
    var nums = t ? (t.match(/\d{3,6}(?:\.\d+)?/g) || []).map(Number) : [];
    return nums.length ? nums[nums.length - 1] : null;
  }

  function coerceNtz(ntz, z, bias) {
    if (!ntz || ntz[0] == null || ntz[1] == null || !z || !z.range || z.range[0] == null || z.range[1] == null)
      return ntz;
    var zlo = Math.min(z.range[0], z.range[1]),
      zhi = Math.max(z.range[0], z.range[1]),
      zmid = (zlo + zhi) / 2;
    var nlo = Math.min(ntz[0], ntz[1]),
      nhi = Math.max(ntz[0], ntz[1]);
    if (zmid >= nlo && zmid <= nhi) {
      if (String(bias).toUpperCase() === "SHORT") nhi = Math.min(nhi, zlo);
      else nlo = Math.max(nlo, zhi);
      return nhi > nlo ? [nlo, nhi] : null;
    }
    return ntz;
  }

  function deriveDir(d) {
    var bias = String((d && d.biasSession) || "").toUpperCase();
    var preds = (d && d.predictions) || [];
    for (var i = 0; i < preds.length; i++) {
      if (preds[i] && preds[i].kind === "direction" && preds[i].indeciso) return "INDECISO";
    }
    var fc = d && d.frameConflict;
    var whip = d && d.whipsawRisk && d.whipsawRisk.score;
    if (fc && fc.on && whip != null && whip >= 0.5) return "INDECISO";
    if (bias === "LONG" || bias === "SHORT") return bias;
    if (bias === "NEUTRAL") return "INDECISO";
    return "";
  }

  function deriveVScore(d) {
    if (d && d.verdictScore != null && !isNaN(+d.verdictScore)) return Math.round(+d.verdictScore);
    if (d && d.vscore != null && !isNaN(+d.vscore)) return Math.round(+d.vscore);
    var z = d && d.zones && d.zones[0];
    if (z && z.confluence != null) {
      // map confluence 0-12 → rough 0-100
      return Math.max(0, Math.min(100, Math.round((+z.confluence / 12) * 100)));
    }
    var conv = String((d && d.conviction) || "").toLowerCase();
    if (conv === "alta") return 78;
    if (conv === "media") return 55;
    if (conv === "baja") return 32;
    return null;
  }

  function predDigest(d) {
    var preds = (d && d.predictions) || [];
    var kinds = [];
    for (var i = 0; i < preds.length && kinds.length < 3; i++) {
      if (preds[i] && preds[i].kind) kinds.push(String(preds[i].kind).slice(0, 8));
    }
    return kinds.length ? kinds.join("+").slice(0, 40) : "";
  }

  function hypTag(d, plan) {
    if (d && d.hypTag) return String(d.hypTag).replace(/[;\s]+/g, "-").slice(0, 28);
    if (d && d.hypothesisId) return String(d.hypothesisId).replace(/[;\s]+/g, "-").slice(0, 28);
    if (plan && plan.hypotheses && Array.isArray(plan.hypotheses) && plan.hypotheses[0]) {
      var h = plan.hypotheses[0];
      return String(h.id || h).replace(/[;\s]+/g, "-").slice(0, 28);
    }
    return "";
  }

  /** Classic-compatible payload (no v2 keys). */
  function buildClassic(sym, d, plan) {
    if (!d) return "";
    var z = (d.zones && d.zones[0]) || null;
    var parts = ["SYM=" + sym, "SESS=" + ((plan && plan.session) || "")];
    var bias = String(d.biasSession || "").toUpperCase();
    if (bias) parts.push("BIAS=" + bias);
    var sig = String((d.verdict && d.verdict.signal) || "").toUpperCase();
    if (sig) parts.push("SIG=" + sig);
    var az = z && saRange(z.range);
    if (az) parts.push("AZ=" + az);
    var bz = saGolden(d, az);
    if (bz) parts.push("BZ=" + bz);
    var inval = saNum(d.invalidation && d.invalidation.level);
    if (inval != null) parts.push("INVAL=" + inval);
    var t1 = saNum(d.scenarioA && d.scenarioA.target);
    if (t1 != null) parts.push("T1=" + t1);
    var t2 = saT2(d, t1, bias);
    if (t2 != null) parts.push("T2=" + t2);
    var rr = saNum(z && z.risk && z.risk.rr);
    if (rr != null) parts.push("RR=" + rr);
    var stop = saStop(z);
    if (stop != null) parts.push("STOP=" + stop);
    var win = saWin(z);
    if (win) parts.push("WIN=" + win);
    var ntz = coerceNtz(d.noTradeZone, z, bias);
    var nt = saRange(ntz);
    if (nt) parts.push("NT=" + nt);
    var fvg = z && z.fvg && z.fvg[0] && saRange(z.fvg[0].range);
    if (fvg) parts.push("FVG=" + fvg);
    if (z && z.fvg && z.fvg[0]) {
      var f0 = z.fvg[0];
      if (f0.dir) parts.push("FVGDIR=" + String(f0.dir).toLowerCase());
      if (f0.tf) parts.push("FVGTF=" + f0.tf);
    }
    var em = saNum(d.expectedMove && d.expectedMove.base);
    if (em != null) parts.push("EM=" + Math.round(em));
    return parts.join(";");
  }

  /** Overlay v2 payload = classic + optional new keys. */
  function buildPayload(sym, d, plan, opts) {
    opts = opts || {};
    var base = buildClassic(sym, d, plan);
    if (!base) return "";
    if (opts.classicOnly) return base;
    // prefer precomputed
    if (d && d.tvPayload && opts.preferInstrumentField) return String(d.tvPayload);
    var extras = [];
    var vs = deriveVScore(d);
    if (vs != null) extras.push("VSCORE=" + vs);
    var fc = d && d.frameConflict;
    extras.push("FCONFLICT=" + (fc && fc.on ? 1 : 0));
    var whip = d && d.whipsawRisk && saNum(d.whipsawRisk.score);
    if (whip != null) extras.push("WHIP=" + whip);
    var dir = deriveDir(d);
    if (dir) extras.push("DIR=" + dir);
    var hyp = hypTag(d, plan);
    if (hyp) extras.push("HYP=" + hyp);
    var pred = predDigest(d);
    if (pred) extras.push("PRED=" + pred);
    return extras.length ? base + ";" + extras.join(";") : base;
  }

  function buildAll(plan, opts) {
    var out = {};
    var inst = (plan && plan.instruments) || {};
    ["NQ", "ES", "GC", "YM", "CL"].forEach(function (sym) {
      if (inst[sym]) out[sym] = buildPayload(sym, inst[sym], plan, opts);
    });
    return out;
  }

  return {
    buildClassic: buildClassic,
    buildPayload: buildPayload,
    buildAll: buildAll,
    L: L,
    saRange: saRange,
  };
});
