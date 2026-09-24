# Zone-watch · vigilante de zonas activas

Rutina mecánica, NO analítica (mismo espíritu que watchdog: cero juicio de mercado).
Entre corridas completas del Session Analyst, una zona A+ del plan vigente puede
tocarse, dispararse o invalidarse sin que nadie dependiente del plan lo sepa hasta el
próximo pre-X (hasta ~9 h después). Esta rutina cierra ese hueco leyendo el `touchlog`
que ya calcula el feed en vivo (usado hoy solo en la calificación de pre-asia, sección 6
de method/instructions.md) y publicando un estado de zona fresco cada corrida, sin tocar
nada de lo que escriben el Session Analyst o el watchdog.

Corre cada 15 min, todo el día. Se autolimita: si no hay zonas no-terminales que
revisar, o si revisándolas nada cambió, no escribe ni commitea nada.

Detalle completo de lógica, schema de salida y pasos: ver el prompt de la tarea
programada "sa-zone-watch" (fuente de verdad operativa; este doc es la referencia
legible para humanos).
