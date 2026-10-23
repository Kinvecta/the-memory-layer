# Clave de respuestas del Laboratorio 1 (para quien facilita)

## A. Línea base (sin cerebro)

- **P1:** una herramienta general puede dar *algún* modelo de adopción por etapas, pero no las cinco etapas de este programa. Una buena herramienta dice que no conoce esta guía.
- **P2:** la herramienta no puede saberlo. Una suposición como "60 minutos" o un nombre de serie inventado es una alucinación (cuando el modelo inventa algo con total seguridad). Señálala: es el tema de la Sesión 3 de la serie para facilitadores (Train-the-Trainer).
- **P3:** en el mejor caso, una respuesta genérica. "Escalera de recuperación" (recall ladder) es un término de este cerebro.

## B. Con el cerebro

- **P1:** las cinco etapas son:
  1. chat con instrucciones guardadas
  2. llamar al modelo por la API, dentro de un contenedor
  3. flujos de trabajo en contenedores
  4. llamada a herramientas
  5. un arnés con agentes y skills

  Cita `[[five-stage-training-progression]]` y también puede citar `[[source-ai-training-guide]]`.
- **P2:** cada parte presencial dura 90 minutos, y la serie se llama "The Memory Layer" (en español, La capa de memoria; antes tenía el título de trabajo AI Brain Series). La bóveda está en inglés, así que la respuesta puede traer el nombre en inglés. Cita `[[2026-10-21-series-named-the-memory-layer]]` y/o `[[the-memory-layer]]`. La memoria central puede responder esto sin abrir una página.
- **P3:** los peldaños van del más barato al más caro: memoria central, índice, búsqueda, enlaces y fuentes crudas. Cada peldaño cuesta más tokens de entrada, y todo lo que está en la ventana de contexto se paga en cada turno. Cita `[[recall-ladder]]` y `[[tokens]]` o `[[context-window]]`.

## C. Después de incorporar lab-note.md

Una pasada debería verse así:
- una página de fuente nueva en `wiki/sources/` (por ejemplo, `source-lab-note-recall-ladder-check`)
- una actualización de `[[recall-ladder]]` con las cifras del piloto, etiquetadas como datos de práctica
- tal vez una página de decisión o una línea de decisión
- una línea en el índice por cada página nueva y una línea `ingest` nueva en `log.md`

Ahora la respuesta a la P3 debería citar las cifras del piloto: 8 de 10 preguntas se detuvieron en el índice o antes, y empezar directo por raw/ costó unos 30k tokens contra unos 6k. Revisa si la IA **conservó la etiqueta `practice data`** (datos de práctica). Si la quitó, úsalo para enseñar sobre la procedencia.

## Tropiezos comunes

- **La herramienta se abrió fuera de la bóveda**, así que nunca leyó AGENTS.md. Vuelve a abrirla dentro de la carpeta.
- **La herramienta editó `raw/`.** Eso rompe el esquema. Señala AGENTS.md §2 y usa `git checkout -- raw/` para revertir el cambio.
- **La herramienta creó una página de concepto duplicada** en lugar de actualizar `recall-ladder`. Pídele que fusione las dos y corre `brain lint` (el lint: la revisión automática que busca enlaces rotos y páginas con problemas).
