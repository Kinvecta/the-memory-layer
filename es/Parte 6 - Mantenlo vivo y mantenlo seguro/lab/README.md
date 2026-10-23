# Laboratorio 6 · Mantenlo vivo y mantenlo seguro

Tiempo: unos 20 minutos. Trabaja en una **copia** de tu bóveda (o de `brain-vault/`) que sea un repositorio git.

| Archivo | Qué es |
|---|---|
| `lab-sheet.md` | La guía del laboratorio: los pasos A a E, con un espacio para cada respuesta |
| `schedule-configs.md` | El latido (heartbeat) en macOS (launchd), Linux (cron) y Windows (Programador de tareas) |
| `lab6_check.py` | Planta dos recortes maliciosos en una copia temporal, corre el lint y el latido, e imprime lo que pasó |
| `expected-output.txt` | Una corrida real de `lab6_check.py` sobre `brain-vault/` |
| `planted-clip.md` | Un recorte con una instrucción visible dirigida a tu IA |
| `invisible-ink.md` | Un recorte con una instrucción escondida en caracteres de etiqueta de Unicode (tinta invisible) |
| `make_invisible.py` | Escribe cualquier oración con tinta invisible, para que pruebes tu propio escáner |
| `answer-key.md` | Respuestas modelo y qué revisar |

Necesitas `brain-tools` de este repositorio ([`../../../brain-tools/`](../../../brain-tools/)), en la versión con los cambios de la Parte 6 (`brain heartbeat --commit`).

## Archivos que se quedan en inglés

- `planted-clip.md` e `invisible-ink.md` se quedan en inglés a propósito, sin cambiar ni un byte. `lab6_check.py` los planta en la bóveda, y el lint y `expected-output.txt` dependen de su contenido exacto (las líneas 7 y 4, y los caracteres ocultos).
- `lab6_check.py`, `make_invisible.py` y `expected-output.txt` también son idénticos a los de la versión en inglés. `expected-output.txt` es lo que imprime el script, así que tu salida se compara línea por línea.
- La bóveda de referencia (`brain-vault/`) y `brain-tools/` son las mismas para la edición en inglés y la edición en español. Por eso los comandos, los nombres de las secciones del reporte y lo que imprimen las herramientas aparecen en inglés.
- Versión en inglés de este laboratorio: [`../../../Part 6 - Keep It Alive and Keep It Safe/lab/`](<../../../Part 6 - Keep It Alive and Keep It Safe/lab/>).
