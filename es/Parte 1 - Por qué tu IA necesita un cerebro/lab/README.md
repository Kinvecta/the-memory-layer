# Laboratorio 1: las mismas preguntas, con y sin cerebro (25 min)

**Objetivo:** ver la diferencia entre una IA sin memoria y la misma IA conectada a un cerebro. Después, ver cómo el cerebro crece con una fuente más.

**Necesitas:**
- Cualquier herramienta de IA que pueda leer y escribir archivos locales: un agente de código, una app de chat de escritorio con un conector de archivos o un asistente del IDE.
- Una **copia** de `../../../brain-vault/`. No trabajes en la copia maestra.
- Opcional: Obsidian, para abrir la copia de la bóveda (bóveda, la carpeta de archivos markdown que forma el cerebro) y ver cómo cambian las páginas.

**Regla de datos:** usa solo la bóveda y `lab-note.md`. No pegues datos reales de tu trabajo.

## Preparación (antes de iniciar el cronómetro)

```bash
cp -R "../../../brain-vault" ~/memory-layer-lab-vault
cd ~/memory-layer-lab-vault && git init -q && git add -A && git commit -qm "lab start"
```

## A. Línea base (5 min)

Abre tu herramienta de IA **fuera** de la bóveda, sin archivos adjuntos. Haz las tres preguntas de `questions.md`. Anota cada respuesta y si la herramienta sonaba segura.

## B. Con el cerebro (8 min)

1. Abre la misma herramienta **dentro** de `~/memory-layer-lab-vault`, para que lea `AGENTS.md`.
2. Haz las mismas tres preguntas.
3. Abre cada `[[citation]]` que te dé. ¿La página dice lo que afirma la respuesta?

## C. Aliméntalo (8 min)

1. Copia `lab-note.md` a la carpeta `inbox/` de la bóveda.
2. Pide la ingesta: "Incorpora inbox/lab-note.md siguiendo skills/brain-ingest/SKILL.md."
3. Vuelve a hacer la pregunta 3. ¿Qué cambió y qué página cita ahora?
4. Lee las últimas líneas de `log.md` y luego corre `git diff --stat`.

## D. Repaso del laboratorio (4 min)

- ¿Qué respuestas cambiaron entre A y B?
- ¿Se sostuvo cada cita?
- ¿Cuántas páginas tocó una sola nota en el paso C?

## Reto extra

Desde `../../../brain-tools`:

```bash
pip install -e .
brain --vault ~/memory-layer-lab-vault search "recall ladder tokens"
brain --vault ~/memory-layer-lab-vault lint
```

## Archivos que se quedan en inglés

- `lab-note.md` se queda en inglés a propósito, sin cambiar ni un byte. Es la fuente que incorporas a la bóveda, y la clave de respuestas depende de su contenido exacto.
- La bóveda de referencia (`brain-vault/`) y `brain-tools/` son las mismas para la edición en inglés y la edición en español. Por eso los nombres de páginas dentro de `[[...]]`, los comandos y lo que imprimen las herramientas aparecen en inglés. Tu IA puede responder en español aunque las fuentes estén en inglés.
- Versión en inglés de este laboratorio: [`../../../Part 1 - Why Your AI Needs a Brain/lab/`](<../../../Part 1 - Why Your AI Needs a Brain/lab/>).
