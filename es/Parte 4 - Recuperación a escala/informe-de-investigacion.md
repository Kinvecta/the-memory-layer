# Informe de investigación · La capa de memoria · Parte 4: Recuperación a escala

Búsqueda por palabras clave, por significado e híbrida. Informe de investigación, 22 oct 2026. Los números entre corchetes remiten a la lista de fuentes. Las citas están traducidas del inglés; los títulos de las fuentes se quedan en su idioma original.

## 1. Cuándo un archivo índice deja de bastar

- **El index.md de Karpathy (gist creado el 4 de abril de 2026).** Él describe index.md como "un catálogo de todo lo que hay en la wiki". El LLM (modelo de lenguaje grande) "lee primero el índice para encontrar las páginas relevantes y luego profundiza en ellas". Su afirmación sobre la escala: "Esto funciona sorprendentemente bien a escala moderada (~100 fuentes, ~cientos de páginas)". Agrega que "a escala pequeña el archivo índice basta, pero conforme crece la wiki conviene una búsqueda de verdad". Para eso recomienda qmd, "un motor de búsqueda local para archivos markdown con búsqueda híbrida BM25/vectorial y reordenamiento con LLM, todo en el dispositivo" [1].
- **La crítica.** El gist "LLM Wiki v2" dice que index.md "funciona hasta quizá 100-200 páginas. Más allá, el propio índice se vuelve demasiado largo para que el LLM lo lea de una pasada, y necesitas una búsqueda de verdad". En una respuesta, el autor ubica el punto de quiebre en "200-500 documentos" [2]. Es la opinión de alguien que lo practica, no una medición.
- **¿Por qué no simplemente cargarlo todo?**
  - *Lost in the Middle* (Liu et al., 2023; TACL 2024) encontró una curva de precisión en forma de U: el medio de un contexto largo es lo que peor se aprovecha. Con GPT-3.5 y 20 documentos, la precisión con la respuesta a la mitad fue de 53.8%. Eso queda *por debajo* de su puntaje a libro cerrado, sin ningún documento (56.1%) [3].
  - *Context Rot* (Chroma, julio de 2025) probó 18 modelos, y el desempeño cayó al crecer la entrada, aun en tareas simples. Un solo distractor ya afectaba. En LongMemEval, los prompts (la instrucción o petición que le das al modelo) enfocados de unos 300 tokens (un token es un pedazo de texto que el modelo lee y escribe) le ganaron a los prompts completos de unos 113k tokens [4].
  - *NoLiMa* (ICML 2025) hizo preguntas con muy poca coincidencia de palabras con la respuesta. A 32K tokens, 10 de 12 modelos de contexto largo cayeron por debajo de la mitad de su puntaje de contexto corto. GPT-4o pasó de 99.3% a 69.7% [5].
  - La regla de Anthropic: con menos de unos 200k tokens (más o menos 500 páginas), simplemente pon todo en el prompt. Por encima de eso, recupera [6].

## 2. BM25

BM25 (búsqueda por palabras clave con puntaje) es la función estándar para ordenar por palabras clave, salida del marco probabilístico de relevancia (Robertson y Zaragoza, 2009) [7]. Es la opción predeterminada en Lucene, Elasticsearch y OpenSearch.

**En palabras simples.** Una página obtiene más puntos cuando usa más las palabras de tu consulta. Esto es la *frecuencia del término*, con rendimientos decrecientes: la décima mención suma mucho menos que la segunda, y **k1** define qué tan rápido se aplana la curva. Las palabras raras cuentan más que las comunes. Esto es la *frecuencia inversa en documentos*: "SQLite" en tu bóveda (la carpeta de archivos markdown que forma el cerebro) es una señal fuerte, mientras que "the" no lo es. Las páginas largas reciben una penalización leve para que no ganen solo por contener más palabras. Esto es la *normalización por longitud*, y **b** (de 0 a 1) define su fuerza.

**Valores típicos.** Elasticsearch y Lucene usan por defecto k1 = 1.2 y b = 0.75 [8]. El rango que más se cita para k1 va de 1.2 a 2.0, así que k1 = 1.4 / b = 0.75 en brain-tools es lo convencional.

**Una línea base sólida.** BEIR (Thakur et al., 2021) probó la recuperación sin entrenamiento previo (zero-shot) en 18 conjuntos de datos y concluyó: "BM25 es una línea base robusta" [9]. En 2025, a BM25 también le fue "muy bien" en LIMIT, donde los modelos de embeddings densos fallaron [10].

**Cuándo ganan las palabras clave.** Nombres exactos, siglas (RMF, ATO), códigos de error (`ORA-01017`), números de ticket, IDs, cadenas de versión y jerga poco común.

## 3. Embeddings y búsqueda semántica

**Qué es un embedding.** Un modelo convierte un texto en un vector, por ejemplo 768 números, que funcionan como las coordenadas de su significado. Un embedding es esa representación numérica del significado de un texto. La *similitud coseno* mide el ángulo entre dos vectores: 1 significa la misma dirección y cerca de 0 significa que no tienen relación. "Car" (carro) y "vehicle" (vehículo) aparecen en contextos parecidos durante el entrenamiento, así que sus vectores apuntan hacia el mismo lado aunque no compartan letras.

**El modelo de brain-tools: nomic-embed-text v1.5** [11][12]
- 137M parámetros y 768 dimensiones, con truncamiento Matryoshka a 512, 256, 128 o 64 dimensiones.
- Contexto nativo de 8,192 tokens. Ollama indica 2K, que alcanza de sobra para fragmentos de 220 palabras.
- Licencia Apache-2.0, con pesos (los valores que el modelo aprendió en su entrenamiento) y datos de entrenamiento abiertos.
- Prefijos obligatorios: "el prompt de texto debe incluir un prefijo con la instrucción de la tarea". Usa `search_query:` para las consultas y `search_document:` para los documentos. Los otros prefijos son `clustering:` y `classification:`.
- Descarga de 274 MB en Ollama.

**Alternativas locales**
- **EmbeddingGemma** (septiembre de 2025): 308M parámetros, 768 dimensiones, contexto de 2K, menos de 200 MB de RAM cuando está cuantizado y más de 100 idiomas. Google lo presenta como el mejor modelo de embeddings multilingüe abierto con menos de 500M parámetros en MTEB [13]. Es el modelo de embeddings predeterminado de qmd [14].
- **Qwen3-Embedding** (0.6B, 4B y 8B; Apache-2.0): contexto de 32K. El modelo de 8B quedó en el primer lugar de MTEB multilingüe con 70.58 al 5 de junio de 2025 [15].
- **bge-m3**: 567M parámetros, contexto de 8K y salida densa, dispersa y multivector [16].
- **mxbai-embed-large**: 670 MB, con un contexto de 512 tokens [17].

**El panorama de MTEB.** Un resumen de marzo de 2026 pone cerca de la cima a Qwen3-Embedding-8B, NV-Embed-v2 (no comercial), Gemini embedding-001 y voyage-3-large. También advierte que MTEB promedia muchos tipos de tareas, así que lee la columna de recuperación nDCG@10 y haz pruebas con tus propios datos [18][19].

**Privacidad.** Con Ollama, tanto el texto de las notas como los vectores se quedan en tu máquina y en tu archivo SQLite local. Ninguna API de embeddings los ve nunca.

**Debilidades.** A los embeddings les cuestan los tokens exactos (IDs, códigos, nombres raros), los números ("presupuesto 2023" vs. "presupuesto 2024") y la negación ("proyectos que *no* usan Postgres" cae cerca de "proyectos que usan Postgres").

**LIMIT** (Weller et al., Google DeepMind y JHU, agosto de 2025) [10]
- El artículo demuestra que un solo vector de dimensión *d* solo puede representar una cantidad limitada de conjuntos distintos de los k mejores resultados.
- Aun con vectores optimizados directamente sobre el conjunto de prueba, el punto de quiebre extrapolado es de unos 500k documentos con d=512 y de unos 1.7M con d=768.
- En un conjunto de datos deliberadamente sencillo, de tipo "¿a quién le gusta X?", a Qwen3, Gemini Embedding, GritLM y E5-Mistral les costó trabajo, mientras que a BM25 le fue muy bien.

## 4. Búsqueda híbrida y fusión recíproca de rankings

**Origen.** Cormack, Clarke y Büttcher, SIGIR 2009: "k = 60 se fijó durante una investigación piloto y no se modificó". Los autores señalan que el valor exacto no es crítico [20].

> **Puntaje RRF(d) = Σ sobre cada lista ordenada r de 1 / (k + posición_r(d)),  k = 60**

**Ejemplo resuelto.** Una página en el lugar 1 según BM25 y en el lugar 3 según los embeddings obtiene 1/61 + 1/63 ≈ 0.032. Una página en el lugar 1 de una sola lista obtiene ≈ 0.016, así que el acuerdo gana. Como la fusión recíproca de rankings (RRF, por sus siglas en inglés) usa solo posiciones, los puntajes de BM25 y los de similitud coseno nunca tienen que estar en la misma escala. brain-tools agrega encima un pequeño bono para que las páginas curadas de la wiki queden por arriba de las fuentes crudas.

**Evidencia**
- **Contextual Retrieval de Anthropic** (septiembre de 2024), que mide la falla como 1 − recall@20 [6]:

  | Configuración | Tasa de falla | Cambio respecto a la línea base |
  |---|---|---|
  | Línea base | 5.7% | — |
  | Embeddings contextuales | 3.7% | −35% |
  | Más BM25 contextual | 2.9% | −49% |
  | Más reordenamiento | 1.9% | −67% |

- **Elastic** (julio de 2023), en promedio sobre BEIR: la híbrida con RRF mejoró nDCG@10 en 18% sobre BM25 y en 1.4% sobre ELSER solo [21].
- **OpenSearch** (febrero de 2025): la híbrida con RRF le ganó a la búsqueda solo neuronal en 6 de 6 conjuntos de BEIR y a BM25 en 5 de 6. La excepción fue TREC-COVID (−3%) [22]. O sea, la híbrida no *siempre* es mejor que BM25.
- **Weaviate** (agosto de 2023): la fusión por puntajes recuperó cerca de 6% más que la fusión por posiciones en FiQA. El método de fusión importa en el margen [23].

**Los rerankers en una línea.** Un reranker (un modelo que reordena los resultados) es más lento: lee la consulta junto con cada candidato y reordena los 50–150 primeros resultados. En la prueba de Anthropic, este paso llevó la reducción de fallas de 49% a 67%.

## 5. Fragmentación

- **Estrategias.** La fragmentación de tamaño fijo corta cada N tokens. La fragmentación recursiva o por encabezados corta en los encabezados, luego en los párrafos y luego en las oraciones. La fragmentación semántica corta donde baja la similitud de embeddings entre oraciones vecinas.
- **Chroma** (julio de 2024): la elección de fragmentación movió la recuperación hasta 9%. Un divisor recursivo logró 88.1 de recall con 200 tokens y 89.5 con 400 tokens. La opción común de 800 tokens con 400 de traslape logró 85.4. El traslape no ayudó a un modelo de embeddings grande, pero sí a uno pequeño. Advertencia: un corpus pequeño y consultas sintéticas [24].
- **NVIDIA** (junio de 2025): los fragmentos del tamaño de una página fueron los más precisos (0.648) y los más consistentes. Tanto 128 como 2,048 tokens rindieron menos, y el mejor tamaño cambió según el conjunto de datos [25].
- **Vectara** (octubre de 2024): "los costos computacionales de la fragmentación semántica no se justifican con mejoras de desempeño consistentes" [26].
- **Qué significa esto para brain-tools.** 220 palabras son unos 290 tokens, lo que cae en el punto ideal de 200–400 tokens. Cortar en los encabezados es estructura gratis, y quitar el traslape coincide con lo que encontró Chroma. qmd, en comparación, usa unos 900 tokens con 15% de traslape [14].
- **Por qué ayudan los resúmenes y los alias.** Un fragmento como "Recortó los costos 20%" no significa nada por sí solo. Anthropic antepone a cada fragmento 50–100 tokens de contexto del documento [6]. Agregar el `summary` y los `aliases` de cada nota a sus fragmentos es una versión barata de eso, sin necesidad de un LLM. También le da a BM25 los sinónimos (por ejemplo "RAG" para "retrieval-augmented generation", la generación aumentada por recuperación).

## 6. Medir la recuperación

**Las métricas en palabras simples**
- **Recall@k:** la proporción de las páginas correctas que quedaron entre las k primeras.
- **MRR:** 1 entre la posición de la primera página correcta (1, 0.5, 0.33…), promediado sobre todas las preguntas.
- **nDCG@k:** premia poner las páginas más relevantes hasta arriba y le da menos peso a las posiciones más bajas. BEIR y MTEB reportan nDCG@10 [9].

**Conjunto de referencia**
- Escribe de 20 a 50 preguntas reales, cada una con la página o las páginas que deberían responderla.
- Mézclalas: más o menos un tercio de términos exactos, un tercio de paráfrasis y un tercio de preguntas que abarcan varias páginas.
- Guárdalas como qrels al estilo de BEIR: `query_id, page_path, relevance`.
- `IDBasedContextRecall` de Ragas compara los IDs recuperados con los IDs de referencia y no necesita un LLM, lo que encaja bien con las rutas de las páginas [27].

**Hoja de calificación.** Usa una fila por pregunta con estas columnas: página esperada; posición con palabras clave, con significado y con la híbrida; hit@5 (sí/no); y 1/posición. Promedia las columnas. Vuelve a correrla después de cualquier cambio en la fragmentación, los alias o k1/b.

## 7. Tarjetas de evidencia

1. **"~100 fuentes, ~cientos de páginas".** El límite del propio Karpathy para usar solo index.md [1].
2. **53.8% < 56.1%.** Una respuesta enterrada salió peor que no tener ningún documento (GPT-3.5) [3].
3. **10 de 12 modelos cayeron por debajo de la mitad de su puntaje de contexto corto a 32K tokens.** GPT-4o pasó de 99.3% a 69.7% [5].
4. **18 de 18 modelos** empeoraron al crecer la longitud de la entrada [4].
5. **−49% / −67%.** Recuperaciones fallidas que se redujeron con embeddings contextuales más BM25, y luego al agregar un reranker [6].
6. **"BM25 es una línea base robusta".** BEIR, en 18 conjuntos de datos [9].
7. **+18% en nDCG@10.** La híbrida con RRF vs. BM25 solo, en promedio sobre BEIR [21].
8. **k = 60**, "se fijó durante una investigación piloto y no se modificó" (2009) [20].

## 8. Analogías para quienes no son del área técnica

1. **BM25 es el índice al final de un libro.** Buscas "ORA-01017" y te manda a la página 212. Las palabras raras son las mejores entradas, y una página que menciona un término cinco veces probablemente trata de eso. *De vuelta al término:* BM25 es un índice automático que le da más peso a las palabras raras y evita que los capítulos largos hagan trampa.
2. **Los embeddings son una bibliotecaria que entiende el sentido.** Le pides algo sobre "arreglar mi carro" y te trae la carpeta de mantenimiento de vehículos, pero titubea con la pieza 4471-B. *De vuelta al término:* los embeddings encuentran sinónimos, pero se les pueden escapar los códigos exactos.
3. **RRF son dos jueces que fusionan sus listas ordenadas.** Uno juzga las palabras y el otro, el significado. Sus puntajes usan escalas distintas, así que no los promedias; premias lo que ambos ponen arriba. *De vuelta al término:* cada lista aporta 1/(60 + posición), así que el acuerdo sube hasta arriba.
4. **La fragmentación son tarjetas de recetas con buenos títulos.** Un capítulo de 40 páginas es difícil de buscar. Una tarjeta titulada "Lasaña (alias pasta al forno), para 8 personas" es fácil de encontrar. *De vuelta al término:* cada fragmento es una tarjeta, y el resumen y los alias son su título y sus apodos.
5. **Un conjunto de evaluación es un examen con clave de respuestas.** Solo sabes si un nuevo método de estudio funciona si vuelves a presentar el mismo examen. *De vuelta al término:* el conjunto de referencia es el examen, Recall@5 y MRR son la calificación, y lo vuelves a presentar después de cada cambio.

## Sin verificar

- Los umbrales de 100–200 y 200–500 páginas vienen de una sola persona que lo practica [2]. No son benchmarks (conjuntos de pruebas).
- No pude confirmar cuál es el primer lugar de MTEB a octubre de 2026. Revisa [19] en vivo.
- No obtuve las cifras exactas de recall@100 de LIMIT ni un benchmark que cuantifique las fallas con la negación.
- Confirmé los valores predeterminados de k1 y b solo con la documentación de Elastic. No obtuve la frase exacta de Robertson y Zaragoza sobre el rango recomendado.

## Fuentes (en inglés)

1. Karpathy, "llm-wiki" gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
2. rohitg00, "LLM Wiki v2": https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
3. Liu et al., "Lost in the Middle": https://arxiv.org/abs/2307.03172
4. Chroma, "Context Rot": https://www.trychroma.com/research/context-rot
5. Modarressi et al., "NoLiMa": https://huggingface.co/papers/2502.05167
6. Anthropic, "Introducing Contextual Retrieval": https://www.anthropic.com/news/contextual-retrieval
7. Robertson & Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond": https://ir.webis.de/anthology/2009.ftir_journal-ir0anthology0volumeA3A4.0/
8. Elasticsearch similarity documentation: https://www.elastic.co/guide/en/elasticsearch/reference/6.x/index-modules-similarity.html
9. Thakur et al., "BEIR": https://arxiv.org/abs/2104.08663
10. Weller et al., "On the Theoretical Limitations of Embedding-Based Retrieval": https://arxiv.org/abs/2508.21038
11. nomic-embed-text-v1.5 model card: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
12. Ollama, nomic-embed-text: https://ollama.com/library/nomic-embed-text
13. Google, "Introducing EmbeddingGemma": https://developers.googleblog.com/introducing-embeddinggemma/
14. tobi/qmd: https://github.com/tobi/qmd
15. Qwen3-Embedding model card: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
16. Ollama, bge-m3: https://ollama.com/library/bge-m3
17. Ollama, mxbai-embed-large: https://ollama.com/library/mxbai-embed-large
18. PremAI, embedding models for RAG (2026): https://www.premai.io/blog/best-embedding-models-for-rag-2026-ranked-by-mteb-score-cost-and-self-hosting/
19. MTEB leaderboard: https://huggingface.co/spaces/mteb/leaderboard
20. Cormack, Clarke & Büttcher, "Reciprocal Rank Fusion" (SIGIR 2009): https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf
21. Elastic, hybrid retrieval: https://www.elastic.co/search-labs/blog/improving-information-retrieval-elastic-stack-hybrid
22. OpenSearch, RRF for hybrid search: https://opensearch.org/?p=4023
23. Weaviate, hybrid search fusion algorithms: https://weaviate.io/blog/hybrid-search-fusion-algorithms
24. Chroma, "Evaluating Chunking Strategies": https://trychroma.com/research/evaluating-chunking
25. NVIDIA, chunking strategy: https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/
26. Qu, Bao & Tu, "Is Semantic Chunking Worth the Computational Cost?": https://arxiv.org/abs/2410.13070
27. Ragas, Context Recall: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_recall/
