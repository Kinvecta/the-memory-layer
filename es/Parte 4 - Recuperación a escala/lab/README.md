# Laboratorio 4 · Indexa, califica, corrige

La capa de memoria, Parte 4: Recuperación a escala. 20 minutos, en una copia de `brain-vault/` con `brain-tools` instalado.

| Archivo | Qué es |
|---|---|
| `lab-sheet.md` | La guía del laboratorio: los pasos A–E para cada participante |
| `golden.csv` | La clave de respuestas (el conjunto de referencia): 6 preguntas, cada una con la página que debería responderla |
| `run_eval.py` | Califica la clave de respuestas en modo por palabras clave, semántico e híbrido: posición, recall@5 y MRR |
| `extra-questions.csv` | 8 preguntas más para practicar |
| `expected-results.md` | Para quien facilita: la salida esperada antes y después de la corrección, y cómo hacer el repaso |

La regla de oro: **Palabras para lo exacto. Significado para las ideas. Fusiona los rankings. Mide cada cambio.**

## Archivos que se quedan en inglés

- `golden.csv`, `extra-questions.csv` y `run_eval.py` se quedan en inglés a propósito, sin cambiar ni un byte. Las preguntas buscan páginas de la bóveda de referencia, que está en inglés. Los resultados esperados dependen de esas mismas palabras.
- Los bloques de salida de `expected-results.md` se quedan en inglés porque son lo que imprime `run_eval.py`.
- Si en el paso E agregas una pregunta en español, la búsqueda por palabras clave casi no encontrará coincidencias en páginas en inglés. Anota qué hace la búsqueda por significado: es una buena comparación.
- Versión en inglés de este laboratorio: [`../../../Part 4 - Recall at Scale/lab/`](<../../../Part 4 - Recall at Scale/lab/>).
