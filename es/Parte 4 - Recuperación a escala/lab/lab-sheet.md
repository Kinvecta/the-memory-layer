# Laboratorio 4 · Indexa, califica, corrige (20 min)

Necesitas:

- una copia de `brain-vault/` (trabaja en la copia, no en el original);
- `brain-tools` instalado: `pip install -e brain-tools`;
- opcional: Ollama con el modelo de embeddings: `ollama pull nomic-embed-text`.

¿No tienes Ollama? Haz todos los pasos de todos modos. Las columnas de significado e híbrida van a repetir la de palabras clave, así que compara tus resultados con alguien a tu lado que sí tenga Ollama.

## A · Indexa (4 min)

```
brain --vault ~/brain-copy index --no-embed     # solo el índice por palabras clave, unos segundos
brain --vault ~/brain-copy index                # agrega vectores (con Ollama corriendo); la primera vez tarda varios minutos
brain --vault ~/brain-copy stats
```

Anota el número de archivos, de fragmentos y de fragmentos con vectores que reporta el índice.

## B · Califica (7 min)

```
python3 run_eval.py ~/brain-copy golden.csv
```

Para cada pregunta, anota la posición de la página correcta en cada modo (`-` significa que no estuvo entre los primeros 20). Luego anota recall@5 y MRR para cada modo.

| Medida | Qué te dice |
|---|---|
| recall@5 | En cuántas de las 6 preguntas la página correcta quedó entre los primeros 5 |
| MRR | El promedio de 1/posición: la posición 1 vale 1, la posición 2 vale 0.5 y un fallo vale 0 |

## C · Explica (3 min)

Elige una fila donde los modos no coincidan. Explica la diferencia en una oración, en términos de **palabras** contra **significado**.

## D · Corrige (4 min)

`crawl walk run` (gatea, camina, corre) es el apodo que usa el equipo para el camino de capacitación de cinco etapas, y todos los modos fallan con él.

1. Abre `wiki/concepts/five-stage-training-progression.md`.
2. Agrega `crawl walk run` al **final** de su lista `aliases:`.
3. Corre `brain index` (solo cambia un archivo).
4. Vuelve a correr `run_eval.py`.

¿Qué cambió en la fila 6? ¿Qué cambió en los totales?

## E · Amplía (2 min)

Agrega a `golden.csv` una pregunta real que le harías a tu propio cerebro, con la página que debería responderla. Califícala.

**Repaso del laboratorio:** ¿qué modo ganó en qué tipo de pregunta? ¿Qué cambió un solo alias?
