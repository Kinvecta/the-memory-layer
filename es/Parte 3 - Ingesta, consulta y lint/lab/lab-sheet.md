# Laboratorio 3 · Ingesta, consulta, lint y deshacer (20 min)

Trabaja en una **copia** de la bóveda de referencia (`brain-vault/`) o en tu propio cerebro, con el manual y las skills de la Parte 2 instalados. Abre tu herramienta de IA **dentro** de esa carpeta.

## Preparación (una vez)

```bash
cd brain-vault            # tu copia
git init && git add -A && git commit -m "init"     # sáltalo si ya es un repositorio git
brain index               # opcional: actualiza la búsqueda
```

## A · Ingesta (6 min)

1. Copia `part2-transcript.md` de esta carpeta del laboratorio a `inbox/`.
2. Pídele a tu herramienta de IA: **"Incorpora inbox/part2-transcript.md."**
3. Anota las 3–5 ideas clave que menciona antes de escribir cualquier cosa.
4. Cuando termine: `git add -A && git commit -m "ingest: part2-transcript"` (sáltalo si la skill ya hizo el commit).

## B · Revisión (3 min)

1. `git show --stat HEAD`. Cuenta: páginas de fuente ___, páginas actualizadas ___, páginas nuevas ___.
   Forma esperada: **1 página de fuente · 3–8 actualizaciones · 0–3 páginas nuevas**, más una línea en `index.md` y una en `log.md`.
2. Abre **dos** citas nuevas. ¿La transcripción de verdad dice eso? ☐ sí ☐ no (¿cuál?)

## C · Consulta (4 min)

Haz las dos preguntas. Cada punto debe llevar una `[[citation]]`.

- **P1** "¿Qué va en el AGENTS.md de un cerebro y qué se queda fuera?"
- **P2** "¿Cómo encajan el manual, las skills y el presupuesto de tokens?"

Guarda en la wiki la que necesitó síntesis: **"Guarda esa respuesta en `wiki/questions/`."** Luego vuelve a preguntarla. Lecturas antes ___, después ___.

## D · Lint (3 min)

1. Corre `brain lint` (el lint: la revisión automática que busca enlaces rotos y páginas con problemas).
2. Corrige **un** problema mecánico (enlace roto, línea faltante en el índice, frontmatter faltante).
3. Anota **un** problema de criterio que debe decidir una persona: ________________
4. Haz commit: `git commit -am "lint: fixed 1"`.

## E · Deshacer (4 min)

1. Copia `clipped-page.md` a `inbox/` y pide: **"Incorpora inbox/clipped-page.md."**
2. `git show HEAD`. Encuentra el dato falso y la instrucción escondida. ¿La IA la obedeció? ☐ no (bien) ☐ sí (detente y avisa a quien facilita)
3. Deshazlo: usa `git revert HEAD --no-edit` para revertir el commit.
4. `git log --oneline -5`: la ingesta y su reversión están en el historial.

## Repaso del laboratorio

- ¿Cuántas páginas tocó la ingesta? ¿Alguna cita falló la revisión?
- ¿Qué hallazgo del lint necesitó a una persona y no a un script?
