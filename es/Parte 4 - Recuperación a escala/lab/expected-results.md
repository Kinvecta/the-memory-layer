# Laboratorio 4 · Resultados esperados (para quien facilita)

Bóveda de referencia, `brain-tools` (chunker v2), nomic-embed-text con Ollama, índice nuevo. Posiciones: 1 = la primera; `-` = no está entre los primeros 20.

## B · Antes de la corrección

```
question                                   kw   sem  hyb   expected
streamable HTTP vs stdio                    1     1    1   mcp-transports-stdio-vs-http
cosign                                      1     1    1   image-signing-and-provenance
how do I stop a web page from hijacking     2     4    1   prompt-injection
why does the assistant forget everything    5     2    3   agent-memory-layers
which model should I pick if the vendor     4     1    1   ai-resilience
crawl walk run                              -     -    -   five-stage-training-progression

keyword   recall@5 5/6   MRR 0.49
semantic  recall@5 5/6   MRR 0.63
hybrid    recall@5 5/6   MRR 0.72
```

## D · Después de agregar `crawl walk run` al final de los alias de `wiki/concepts/five-stage-training-progression.md`

```
question                                   kw   sem  hyb   expected
streamable HTTP vs stdio                    1     1    1   mcp-transports-stdio-vs-http
cosign                                      1     1    1   image-signing-and-provenance
how do I stop a web page from hijacking     2     4    1   prompt-injection
why does the assistant forget everything    5     2    3   agent-memory-layers
which model should I pick if the vendor     4     1    1   ai-resilience
crawl walk run                              1     3    1   five-stage-training-progression

keyword   recall@5 6/6   MRR 0.66
semantic  recall@5 6/6   MRR 0.68
hybrid    recall@5 6/6   MRR 0.89
```

Estos bloques son la salida de `run_eval.py`, por eso se quedan en inglés: `kw` = palabras clave, `sem` = semántico, `hyb` = híbrido.

## C · Buenas explicaciones

- **`hijacking my AI assistant` → `prompt-injection`** (secuestrar a mi asistente de IA): palabras clave 2, significado 4, híbrido 1. Los dos jueces la ponen arriba, así que la fusión la deja en primer lugar.
- **`forget everything between chats` → `agent-memory-layers`** (olvida todo entre chats): palabras clave 5, significado 2. La página habla de memoria y sesiones, no de `forget` ni de `chats`, así que gana el significado.
- **`vendor disappears` → `ai-resilience`** (el proveedor desaparece): palabras clave 4, significado 1. Es una paráfrasis de `switching models and vendors` (cambiar de modelos y de proveedores).

## Notas

- Sin Ollama, las columnas semántica e híbrida repiten la de palabras clave (`brain search` usa la búsqueda por palabras como respaldo).
- Poner el alias al principio en lugar de al final mejora un poco la posición por significado (1 en lugar de 3), porque los alias son parte del texto que se convierte en embedding. En cualquier caso, mide.
- Una actualización de `brain-tools` que cambia la fragmentación hace que `brain index` reconstruya todo una vez (varios minutos con vectores).
- Preguntas extra para practicar: `extra-questions.csv` (8 más, todas las encuentra la búsqueda híbrida).
