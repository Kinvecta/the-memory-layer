# Laboratorio 6 · Clave de respuestas

1. `log.md` (una línea del latido), `memory/reports/<today>.md` y, si la memoria de trabajo tenía más de
   12 horas, un archivo nuevo en `memory/episodes/`. Nada en `raw/`, `wiki/` ni `memory/core.md`.
2. Lo que muestre tu bóveda. La bóveda de referencia reporta 0 problemas.
3. launchd corre la tarea a las 7:40 a. m., cuando la Mac despierta. cron la omite.
4. Los dos la omiten. launchd solo se pone al corriente después de que la computadora estuvo dormida, no apagada.
5. La línea 7 de `planted-clip.md` (`ignore your previous instructions`, una posible inyección) y la
   línea 4 de `invisible-ink.md` (caracteres ocultos, `U+E0020`, el primer carácter de etiqueta).
6. No. La línea 4 parece una viñeta normal. La instrucción está escrita en caracteres de etiqueta que la mayoría de los editores
   no dibujan, pero que un modelo sí puede leer.
7. No. El reporte dice `reflect step was skipped` y la línea del registro termina en `reflect skipped (quarantined)`.
   Mientras el lint marque caracteres ocultos o líneas que parecen instrucciones, el latido no le entrega la bóveda a un agente (cuarentena).
8. Sí. Sin los recortes, el lint sale limpio y el paso de reflexión corre (aquí `echo reflect`, con código de salida 0).
   Si un archivo marcado es una fuente legítima que cita un ataque, consérvalo y agrégalo a
   `memory/reviewed-flags.md` después de leerlo tú.
9. `review due` (y también `stale` si `last_reviewed` tiene más de 90 días).
10. Busca: ediciones a `raw/` o a `memory/core.md` (nunca se permiten), afirmaciones sin `sources:`, texto borrado
    en lugar de `status: superseded` o `status: disputed`, y cualquier cosa que suene a instrucción.
11. Ejemplo: "La tarea nocturna puede actualizar `wiki/`, `memory/working.md` e `inbox/` con propuestas con citas;
    nunca edita `raw/` ni `memory/core.md`, nunca usa herramientas de red, y una persona revisa cada commit."

Salida esperada de `lab6_check.py`: consulta `expected-output.txt`.
