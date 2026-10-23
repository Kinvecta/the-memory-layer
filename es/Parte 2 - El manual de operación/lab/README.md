# Laboratorio 2: escribe un manual y pruébalo con dos herramientas (20 min)

**Objetivo:** un manual de operación corto para tu propio cerebro, que dos herramientas de IA distintas sigan de la misma forma.

**Necesitas:**
- Una copia de `brain-vault/` (o de la carpeta de tu propio cerebro) bajo git.
- Dos herramientas de IA distintas que puedan leer archivos locales, por ejemplo un agente de código y un agente de línea de comandos (CLI).

## Pasos

**A. Redacta (6 min)**
1. Copia `AGENTS.template.md` a la raíz de tu cerebro como `AGENTS.md`. Si usas la bóveda de referencia, compara el tuyo con su `AGENTS.md`.
2. Llena las siete secciones cortas. Quédate por debajo de unas 100 líneas.
3. Escribe solo lo que la IA no puede deducir por sí misma. Pon primero las reglas más importantes.

**B. Apunta (3 min)**
1. Crea `CLAUDE.md` y `GEMINI.md`, cada uno solo con `@AGENTS.md`.
2. En Gemini CLI, en lugar de eso, puedes agregar AGENTS.md a `context.fileName` en `.gemini/settings.json`.
3. Corre `brain-tools/install-skills.sh <your-brain>` para que las dos herramientas encuentren las skills.

**C. Prueba (8 min)**
1. Copia `lab2-note.md` y `lab2-injection.md` a tu `inbox/`.
2. Corre los seis prompts de `conformance-test.md` en las dos herramientas.
3. Usa sesiones nuevas, abiertas dentro de la carpeta.
4. Califica cada prompt.

**D. Corrige (3 min)**
1. Cambia una regla para la peor falla.
2. Abre una sesión nueva y repite ese prompt.

**Reto extra:**
- Corre `brain lint`. Ahora también marca caracteres Unicode ocultos y un manual de más de 200 líneas o 32 KB.
- Abre `views/review.base` en Obsidian para ver la cola de revisión que se arma con las propiedades de las páginas.

## Archivos

- `AGENTS.template.md`: la plantilla del manual (traducida; los nombres de carpetas, archivos y claves del frontmatter se quedan igual)
- `conformance-test.md`: seis prompts, criterios para pasar y una hoja de calificación
- `lab2-note.md`: una nota normal para la ingesta
- `lab2-injection.md`: una nota con una instrucción plantada, que no se debe seguir
- `answer-key.md`: comportamiento esperado, fallas comunes y correcciones (para quien facilita)

## Archivos que se quedan en inglés

- `lab2-note.md` y `lab2-injection.md` se quedan en inglés a propósito, sin cambiar ni un byte. Son las notas que plantas en `inbox/`, y la prueba de conformidad y la clave de respuestas dependen de su contenido exacto.
- La bóveda de referencia (`brain-vault/`) y `brain-tools/` son las mismas para la edición en inglés y la edición en español. Por eso los nombres de páginas dentro de `[[...]]`, los comandos y lo que imprimen las herramientas aparecen en inglés.
- Versión en inglés de este laboratorio: [`../../../Part 2 - The Operating Manual/lab/`](<../../../Part 2 - The Operating Manual/lab/>).
