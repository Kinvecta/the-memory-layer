# Informe de investigación · La capa de memoria · Parte 3: Ingesta, consulta y lint

*La capa de memoria, Parte 3: hacer que el conocimiento se acumule. Investigado el 21 de octubre de 2026. Cada afirmación está ligada a una fuente de la lista al final. Lo que no pude verificar está marcado como no verificado. Las citas textuales están traducidas del inglés; las frases para diapositivas incluyen también el original.*

## 1. El patrón LLM Wiki (Karpathy, abril de 2026)

Karpathy publicó "LLM Knowledge Bases" en X a principios de abril de 2026 y después compartió el gist `llm-wiki` el **4 de abril de 2026** [1][2]. El gist describe tres operaciones:

- **Ingesta:** "Dejas una fuente nueva en la colección cruda y le dices al LLM que la procese". Un LLM es un modelo de lenguaje grande. Agrega que "una sola fuente puede tocar 10-15 páginas de la wiki". *Nuestro curso dice 3–8 páginas por ingesta. Es más conservador que la cifra de Karpathy, así que explica que es una decisión deliberada para principiantes.*
- **Consulta:** "Haces preguntas contra la wiki". También dice que "las buenas respuestas se pueden archivar de vuelta en la wiki como páginas nuevas".
- **Lint:** "De vez en cuando, pídele al LLM que le haga una revisión de salud a la wiki". El lint es la revisión automática que busca enlaces rotos y páginas con problemas. Karpathy señala que el LLM también es bueno para sugerir nuevas preguntas y nuevas fuentes que buscar.
- **index.md** es "un catálogo de todo lo que hay en la wiki", y "el LLM lo actualiza en cada ingesta". **log.md** es "un registro, de solo agregar, de lo que pasó y cuándo".

**Frases cortas para diapositivas (todas del gist [2]):**
- "el LLM redescubre el conocimiento desde cero en cada pregunta." ("the LLM is rediscovering knowledge from scratch on every question.")
- "El conocimiento se compila una vez y luego se mantiene al día, no se vuelve a derivar en cada consulta." ("The knowledge is compiled once and then kept current, not re-derived on every query.")
- "la wiki es un artefacto persistente que se acumula." ("the wiki is a persistent, compounding artifact.")
- "Obsidian es el IDE; el LLM es el programador; la wiki es el código fuente." ("Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.")
- "La wiki es solo un repositorio de git con archivos markdown." ("The wiki is just a git repo of markdown files.")
- "El trabajo de la persona es curar las fuentes, dirigir el análisis, hacer buenas preguntas y pensar qué significa todo eso." ("The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means.")

**Escala y recepción.** Reseñas secundarias calculan su propia wiki en unos 100 artículos y 400K palabras [3][4]. No pude abrir la publicación original en X para confirmar esa cifra. Sanity dice que la publicación se acercó a 22M de vistas [4]. Una revisión de arquitectura reporta 5,000 estrellas en el gist en ocho días y unas 15 implementaciones en la primera semana [5]. Esa cifra es secundaria y no está verificada.

**Implementaciones de la comunidad:** Astro-Han/karpathy-llm-wiki (Agent Skills para Claude Code, Cursor y Codex) [6], toolboxmd/karpathy-wiki [7], GD4AI/obsidian-llm-wiki (un complemento de Obsidian) [8] y el tema `llm-wiki` en GitHub [9].

**Críticas que vale la pena enseñar:** el archivo de esquema (CLAUDE.md o AGENTS.md) es la verdadera "especificación del compilador"; los archivos de índice simples, según se reporta, dejan de escalar después de unas 200 páginas; y nada marca las afirmaciones viejas como obsoletas o reemplazadas [5]. Algunos equipos encontraron que las ingestas simultáneas bifurcaban la wiki y que las reconstrucciones sobrescribían las correcciones humanas [4].

## 2. "Compilar una vez" vs. "recuperar cada vez": la evidencia honesta

**A favor de compilar:**
- **GraphRAG** (Microsoft, 2024) construye por adelantado un grafo de entidades y resúmenes por comunidad. En preguntas de comprensión global sobre corpus de 1M de tokens (un token es un pedazo de texto que el modelo lee y escribe), superó a RAG (generación aumentada por recuperación) vectorial en exhaustividad (una tasa de victorias de alrededor de 72–83%) y en diversidad. Sus resúmenes de nivel raíz usaron solo cerca de 2–3% de los tokens [10].
- **RAPTOR** (ICLR 2024) construye por adelantado un árbol de resúmenes recursivos. Combinado con GPT-4, mejoró "el mejor desempeño en el benchmark QuALITY en 20% de precisión absoluta" [11]. Un benchmark es un conjunto de pruebas.

**En contra, o con resultados mixtos (estudios de 2026 que prueban directamente el LLM Wiki):**
- Una comparación prerregistrada (Cochran, arXiv 2605.18490; 24 papers, 13 preguntas) encontró que la wiki era mejor para la síntesis entre varios papers. Sin embargo, la wiki usó **cerca de 21× más tokens por consulta**, el RAG simple la igualó en datos puntuales, y "el ganador dependía de la línea base, del evaluador y del juez" [12].
- **WiCER** (Huerta, arXiv 2605.07068) encontró que compilar a ciegas **comprimía de más**: una meta de 50% de la longitud produjo 12%. Las respuestas incorrectas subieron a 53–60%, contra 17% con los documentos crudos. Un ciclo de compilar, evaluar y refinar (en la práctica, el lint) bajó las respuestas incorrectas de 55% a 25% [13].
- Una ablación de carga progresiva en una wiki de **709 páginas** mantenida por un LLM encontró que servir primero un índice, más una herramienta de recuperación, bajó el costo por respuesta **30–58%** sin perder calidad [14].

**Conclusión para enseñar.** Compilar gana en síntesis y en respuestas que vas a reutilizar. La recuperación sobre fuentes crudas sigue ganando en datos exactos. Por eso la escalera de recuperación termina en **raw/** y por eso el lint es esencial: el lint es lo que atrapa los datos que se pierden al comprimir. Quienes practican Zettelkasten le ponen nombre a la falla del otro lado: la **"falacia del coleccionista"** (Collector's Fallacy): "'saber de algo' no es lo mismo que 'saber algo'" [15].

## 3. Confiabilidad de los resúmenes y de las citas

- **Vectara Hallucination Leaderboard** (resúmenes de más de 7,700 artículos, actualizado el 11 de mayo de 2026): las tasas de alucinación (cuando el modelo inventa algo con total seguridad) van de **1.8% a 24.2%**, y los modelos de frontera están alrededor de 5–12% (GPT-5.4 con 7.0%, Claude Sonnet 4.6 con 10.6%) [16]. Las tasas suben con la longitud y la complejidad del documento [17].
- **Tow Center / CJR (marzo de 2025):** se les pidió a 8 herramientas de búsqueda con IA identificar la fuente de 200 fragmentos de noticias. Se equivocaron más del **60%** de las veces, desde Perplexity con 37% hasta Grok 3 con 94%. De las 134 respuestas incorrectas de ChatGPT, solo 15 expresaron alguna duda [18][19].
- **EBU/BBC (octubre de 2025):** más de 3,000 respuestas de asistentes, revisadas por 22 emisoras públicas de 18 países. **45%** tenía un problema significativo y **31%** tenía problemas serios con las fuentes [20].
- **Verificabilidad de la búsqueda generativa** (Liu et al., EMNLP 2023): solo **51.5%** de las oraciones estaban totalmente respaldadas por sus citas, y **74.5%** de las citas respaldaban su oración [21].
- **Referencias inventadas** (Walters & Wilder, *Sci. Reports* 2023): 55% de las citas de GPT-3.5 y 18% de las de GPT-4 eran inventadas. De las reales, 43% y 24% respectivamente tenían errores importantes [22].

**Por qué "cita cada afirmación" más una revisión humana al azar.** Una cita hace que una afirmación se pueda revisar, pero estos estudios muestran que las citas muchas veces están mal, y que incluso los jueces LLM no se ponen de acuerdo sobre qué tan fundamentada está una respuesta (ρ = 0.04 en [12]). Por eso una persona debe abrir 2–3 citas por ingesta.

## 4. Actualiza antes de crear: resolución de entidades y deduplicación

- **Mem0** (2025) formaliza "buscar antes de crear": para cada hecho nuevo recupera las 10 memorias más parecidas, y el LLM elige **ADD / UPDATE / DELETE / NOOP** [23]. En términos de ingesta: actualiza la página existente y crea una nueva solo si nada coincide.
- **Neo4j Agent Memory** normaliza los nombres, fusiona automáticamente con un puntaje de 0.90 o más, *marca para revisión* entre 0.85 y 0.90, y trata la similitud de embeddings (representaciones numéricas del significado de un texto) "como una pista, no como una prueba" [24]. Enseña la misma regla: cuando hay duda, el agente propone fusionar y la persona decide.
- **Aviso (callout) de conflicto** (sintaxis de Obsidian [25]). Pon `> [!warning] Conflict` en la primera línea de una cita en bloque; `caution` y `attention` son alias. Un `-` después del tipo, como en `> [!warning]-`, hace que el aviso empiece plegado. Patrón sugerido:
  ```
  > [!warning] Conflict: launch date
  > [[source-a]] says March 2026; [[source-b]] says June 2026. Unresolved.
  ```
  En español, el texto del aviso diría: "Conflicto: fecha de lanzamiento. [[source-a]] dice marzo de 2026; [[source-b]] dice junio de 2026. Sin resolver." Conservar ambas afirmaciones sigue la lección de Sanity: las decisiones sobre conflictos tienen que sobrevivir a las reconstrucciones [4].

## 5. Lint para bases de conocimiento

**Revisiones mecánicas:**
- La **CLI de Obsidian** (línea de comandos, introducida en la 1.12, febrero de 2026) tiene los comandos `orphans`, `deadends` y `unresolved`, más `backlinks`, `properties` y `search` [26]. El CEO de Obsidian, kepano, afirmó que el comando `orphans` es "54x más rápido que grep, 70,000x más barato que MCP" [27]. Es una afirmación del proveedor, hecha en una publicación de X.
- El complemento de la comunidad **"Find orphaned files and broken links"** [28].
- La consulta de Dataview para páginas huérfanas: `list from "" where length(file.inlinks) = 0 and length(file.outlinks) = 0` [29].
- **Obsidian Bases** (complemento central desde la 1.9, mayo de 2025) da vistas de tabla filtradas por propiedades [30]. Úsalo para fechas `updated:` viejas o frontmatter (el bloque de propiedades al inicio de cada página) faltante.

**Equivalentes de docs-as-code (documentación tratada como código):**
- **lychee**: un verificador de enlaces en Rust para Markdown y HTML [31].
- **markdownlint**: reglas de estructura y estilo para Markdown [32].
- **Vale**: lint de redacción basado en reglas [33].

**Por qué se pudren los enlaces.** Pew (2024) encontró que **38%** de las páginas web de 2013 ya no existían en 2023, y que **54%** de las páginas de Wikipedia tienen al menos un enlace de referencia roto [34]. Es un argumento para guardar una copia inmutable de cada fuente en raw/, en lugar de solo una URL.

Las revisiones de criterio (contradicciones, conceptos faltantes, afirmaciones sin cita) necesitan al LLM. Usa el ciclo de sondear y reparar de WiCER como evidencia de que valen la pena [13].

## 6. Git como botón de deshacer

- **Los checkpoints de Claude Code** (`/rewind` o Esc Esc) *no* registran los cambios hechos con Bash ni la mayoría de las ediciones de subagentes, y la documentación dice que "no reemplazan el control de versiones" [35]. **Los checkpoints de Cursor** son locales, se limpian solos y "no son control de versiones" [36].
- **Aider:** "Cada vez que aider edita un archivo, hace commit de esos cambios con un mensaje descriptivo". `/undo` descarta el último cambio y `/diff` lo muestra para revisarlo [37]. Es un precedente de un proveedor para hacer un commit por operación.
- **Git worktrees:** el `--worktree` de Claude Code le da a cada sesión paralela su propia rama y sus propios archivos, "así que las ediciones de una sesión nunca tocan los archivos de otra" [38]. Úsalo para correr dos ingestas en paralelo de forma segura.
- **`git revert` vs `reset`.** `revert <sha>` agrega un commit nuevo que deshace una ingesta mala y conserva el historial. `reset --hard` borra el historial. Enseña a revertir con revert de forma predeterminada.

## 7. Riesgos propios de la ingesta (breve, porque la Parte 6 los cubre)

- **Inyección de prompts** (instrucciones escondidas en un contenido que toman el control del comportamiento de la IA). OWASP LLM01:2025: "Las inyecciones indirectas de prompts ocurren cuando un LLM acepta entradas de fuentes externas, como sitios web o archivos". Mitigaciones: marcar el contenido externo como no confiable y exigir aprobación humana para las acciones privilegiadas [39]. El origen académico es Greshake et al. 2023 [40]. Anthropic reportó una tasa de éxito de ataques de **23.6%** en 123 pruebas para su agente de navegador, que bajó a **11.2%** con mitigaciones [41].
- **Capturar de más.** Ve la falacia del coleccionista [15]. WiCER muestra la falla contraria: comprimir de más [13]. El presupuesto de páginas 1 / 3–8 / 0–3 protege contra las dos.

## 8. Tarjetas de evidencia

1. **"60%+ incorrectas"**: las herramientas de búsqueda con IA identificaron mal la fuente de fragmentos de noticias en más de 60% de las pruebas [18].
2. **"45% / 31%"**: proporción de respuestas de IA sobre noticias con un problema significativo, y con problemas serios de fuentes [20].
3. **"51.5%"**: proporción de oraciones de búsqueda generativa totalmente respaldadas por sus citas [21].
4. **"1.8–24.2%"**: tasas de alucinación al resumir un solo documento; los modelos de frontera están en cerca de 5–12% [16].
5. **"55% → 25%"**: respuestas incorrectas de una wiki compilada antes y después de compilar, evaluar y refinar (lint) [13].
6. **"21×"**: tokens por consulta de un agente con wiki vs. RAG de una sola ronda. Compilar tiene un costo [12].
7. **"38%"**: proporción de páginas web de 2013 que ya no existían en 2023; por eso guardas copias en raw/ [34].
8. **"23.6% → 11.2%"**: tasa de éxito de la inyección de prompts antes y después de las mitigaciones [41].

## Analogías para quienes no son de ingeniería

1. **Ingesta = una bibliotecaria que acomoda un libro nuevo.** Actualiza el catálogo de fichas (index.md), agrega referencias cruzadas a los estantes relacionados (páginas de conceptos) y lo anota en el registro de adquisiciones (log.md). *Conexión con el curso:* una página de fuente, 3–8 páginas actualizadas, más entradas en el índice y en el registro.
2. **Compilar vs. recuperar = un libro mayor vs. una caja de zapatos con recibos.** RAG escarba en la caja de zapatos para cada pregunta. La wiki es el libro mayor, que se cuadra conforme llega cada recibo. La caja de zapatos (raw/) se queda para las auditorías.
3. **Buscar antes de crear = los expedientes de pacientes de un hospital.** Antes de abrir un expediente nuevo, la persona de admisión revisa si "Bob Smith, fecha de nacimiento…" ya existe. Los expedientes duplicados son como ocurren los errores. *Conexión con el curso:* ADD, UPDATE o NOOP; cuando hay duda, marca el posible duplicado para revisión.
4. **Lint = un corrector ortográfico más un editor.** El corrector encuentra de forma mecánica los enlaces rotos y las páginas huérfanas. El editor nota que el capítulo 3 contradice al capítulo 7. Necesitas los dos.
5. **Git = control de cambios con máquina del tiempo.** Cada ingesta es una edición registrada que puedes revisar y rechazar. `revert` es "deshacer, con una nota que dice que lo deshiciste", nunca arrancar páginas.

## Fuentes (en inglés)

1. Karpathy, "LLM Knowledge Bases" (X) https://x.com/karpathy/status/2039805659525644595
2. Karpathy, llm-wiki gist https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
3. DAIR.AI Academy https://academy.dair.ai/blog/llm-knowledge-bases-karpathy
4. Sanity, "Taking Karpathy's wiki to work" https://www.sanity.io/blog/taking-karpathys-wiki-to-work
5. "The Schema Is the Product" https://cozypet.github.io/llm-wiki-schema/
6. https://github.com/Astro-Han/karpathy-llm-wiki
7. https://github.com/toolboxmd/karpathy-wiki/tree/main/
8. https://github.com/gd4ai/obsidian-llm-wiki
9. https://github.com/topics/llm-wiki
10. Edge et al., GraphRAG https://arxiv.org/html/2404.16130v2
11. Sarthi et al., RAPTOR https://www.arxiv.org/abs/2401.18059
12. Cochran, RAG vs LLM-Compiled Wiki https://arxiv.org/abs/2605.18490
13. Huerta, WiCER https://arxiv.org/html/2605.07068
14. Cochran, Progressive Disclosure ablation https://arxiv.org/html/2607.04576
15. Tietze, "The Collector's Fallacy" https://www.zettelkasten.de/posts/collectors-fallacy
16. Vectara leaderboard https://github.com/vectara/hallucination-leaderboard
17. Vectara, next-gen leaderboard https://vectara.com/blog/introducing-the-next-generation-of-vectaras-hallucination-leaderboard
18. CJR Tow Center https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php
19. Nieman Lab https://www.niemanlab.org/2025/03/ai-search-engines-fail-to-produce-accurate-citations-in-over-60-of-tests-according-to-new-tow-center-study/
20. EBU/BBC News Integrity report https://www.bbc.co.uk/aboutthebbc/documents/news-integrity-in-ai-assistants-report.pdf (summary: https://www.infodocket.com/2025/10/22/bbc-largest-study-of-its-kind-shows-ai-assistants-misrepresent-news-content-45-of-the-time-regardless-of-language-or-territory/)
21. Liu et al., Verifiability in Generative Search Engines https://arxiv.org/abs/2304.09848v2
22. Walters & Wilder 2023 https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/
23. Mem0 paper https://arxiv.org/pdf/2504.19413
24. Neo4j Agent Memory, resolution and dedup https://neo4j.com/labs/agent-memory/explanation/resolution-deduplication/
25. Obsidian Help, Callouts https://obsidian.md/help/callouts
26. Obsidian CLI guide https://www.dsebastien.net/the-complete-guide-to-the-obsidian-cli-everything-you-can-do-from-the-terminal/
27. kepano (X) https://x.com/kepano/status/2022305748735381751
28. https://community.obsidian.md/plugins/find-unlinked-files
29. Obsidian forum, Find orphan notes https://forum.obsidian.md/t/find-orphan-notes/817/15
30. Obsidian 1.9.0 changelog https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0
31. lychee https://github.com/lycheeverse/lychee
32. markdownlint https://github.com/DavidAnson/markdownlint
33. Vale https://vale.sh/
34. Pew, "When Online Content Disappears" https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/
35. Claude Code checkpointing https://code.claude.com/docs/en/checkpointing
36. Cursor checkpoints https://docs.cursor.com/agent/chat/checkpoints
37. Aider git docs https://aider.chat/docs/git.html
38. Claude Code worktrees https://code.claude.com/docs/en/worktrees.md
39. OWASP LLM01:2025 https://genai.owasp.org/llmrisk/llm01-prompt-injection/
40. Greshake et al. 2023 https://arxiv.org/abs/2302.12173v2
41. Anthropic Claude for Chrome (via Simon Willison) https://simonwillison.net/2025/Aug/26/piloting-claude-for-chrome/
