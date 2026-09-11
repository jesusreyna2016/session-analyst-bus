# APPLY · Session Analyst STEROIDS v2

Paquete drop-in bajo `/workspace/sa-steroids/`. **No** hace falta clonar de nuevo: copia
estos archivos al repo bus `session-analyst-bus` (branch `main`).

## 0 · Preflight

- Repo local del bus limpio o con cambios commiteables.
- TradingView account (para pegar el Pine).
- Host estático donde ya vive (o vivirá) el Command Center (Netlify / tradedadlog.com).

## 1 · Copiar al bus

Desde la raíz del checkout de `session-analyst-bus`:

```bash
# Ajusta STEROIDS_SRC al path del paquete
STEROIDS_SRC=/workspace/sa-steroids

# Método (upgrade — reemplaza)
cp "$STEROIDS_SRC/method/instructions.md" method/instructions.md
cp "$STEROIDS_SRC/method/watchdog.md"     method/watchdog.md
mkdir -p method
cp "$STEROIDS_SRC/method/payload-schema.md" method/payload-schema.md

# Overlay + HUD + scripts + fixtures (artefactos nuevos first-class)
mkdir -p overlay hud scripts fixtures
cp "$STEROIDS_SRC/overlay/sa_plan_overlay_v2.pine" overlay/
cp "$STEROIDS_SRC/hud/command-center-2.html"       hud/
cp "$STEROIDS_SRC/hud/tv-payload.js"               hud/
cp "$STEROIDS_SRC/scripts/build-tv-payload.mjs"    scripts/
cp "$STEROIDS_SRC/fixtures/sample-payloads.txt"    fixtures/
cp "$STEROIDS_SRC/fixtures/plan-snippet.json"      fixtures/

# Docs del paquete (opcionales pero útiles en el bus)
cp "$STEROIDS_SRC/README-STEROIDS.md" .
cp "$STEROIDS_SRC/APPLY.md" .
```

Actualiza el `README.md` del bus con una línea apuntando a Overlay + HUD 2.0 (no lo
sobreescribas entero).

## 2 · Commit

```bash
git checkout main && git pull --rebase --autostash origin main
git add method/ overlay/ hud/ scripts/ fixtures/ README-STEROIDS.md APPLY.md
git commit -m "steroids v2: overlay+hud+payload bridge + method upgrade"
# push con el mismo patrón del bus (rebase loop)
for i in $(seq 1 6); do git pull --rebase --autostash && git push && break; sleep 5; done
git log origin/main -1 --oneline
```

## 3 · Pegar Pine en TradingView

1. TradingView → Pine Editor → New → pega `overlay/sa_plan_overlay_v2.pine`.
2. Save as **SA Plan Overlay v2**, Add to chart (NQ/ES/GC/YM/CL o micros).
3. Input **Plan payload**: pega una línea de `fixtures/sample-payloads.txt` (classic o v2).
4. Crea alertas desde el indicador (`SA - Zona A+`, `SA - SL`, `SA - T1`, `SA - T2`,
   `SA - inval break`, `SA - +1R→BE`).

## 4 · Hostear HUD 2.0

Opciones:

- **Junto al bus en Netlify**: publica `hud/command-center-2.html` como
  `/command-center-2.html` (o carpeta `hud/`). El botón Fetch busca
  `../plans/latest.json` y `../live/health.json` — ajusta paths si tu publish root difiere.
- **Junto a** `tradedadlog.com/command-center.html`: sube
  `command-center-2.html` + `tv-payload.js` al mismo origen para evitar CORS.
- **Offline**: abre el HTML y usa los file inputs (Plan JSON + Health JSON).

CORS: `fetch` a `raw.githubusercontent.com` desde un origen web puede fallar; preferir el
mismo host que sirve el bus espejo, o file inputs.

## 5 · Dual-run (classic + v2)

1. Deja el CC viejo intacto (sigue construyendo payloads clásicos desde el plan JSON).
2. En una corrida SA nueva, el método STEROIDS pide `instruments.<SYM>.tvPayload` + líneas
   `TV …` en `digest.txt`.
3. Verifica:

```bash
node scripts/build-tv-payload.mjs plans/latest.json
node scripts/build-tv-payload.mjs plans/latest.json --classic
```

4. Pega classic en un chart TV, v2 en otro, confirma que AZ/NT/FVG/INVAL coinciden.
5. Cuando Overlay v2 esté estable, el HUD 2.0 puede ser el default de copy-TV.

## 6 · Checklist post-apply

- [ ] `method/instructions.md` en el bus contiene secciones **6.2 Overlay v2** y **6.3 checklist**
- [ ] Pine compila sin error en TV v6
- [ ] HUD carga un `plans/latest.json` real y copia payload
- [ ] Classic payload de fixtures sigue parseable
- [ ] Watchdog schema de `live/health.json` sin cambios breaking

## Rollback

```bash
git revert <commit-steroids>
# o restaura method/instructions.md desde el commit previo
```

El Pine/HUD nuevos se pueden borrar sin romper el bus de datos (planes/state/live).
