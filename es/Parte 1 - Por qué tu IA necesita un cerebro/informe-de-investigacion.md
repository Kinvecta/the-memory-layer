# Informe de investigación · La capa de memoria · Parte 1: Por qué tu IA necesita un cerebro

Compilado el 21 de octubre de 2026 para La capa de memoria. Las fuentes están al final. Vuelve a verificar
las versiones de las herramientas antes de enseñar con este informe.

## 1. La idea central

Un segundo cerebro es una carpeta de archivos markdown (texto plano con formato sencillo) que tanto las
personas como los arneses de IA pueden leer y escribir. El arnés (en inglés, harness) es el software que
rodea al modelo y decide qué puede ver y hacer. Obsidian es la interfaz más popular porque agrega wikilinks
(enlaces internos entre páginas), enlaces entrantes, vista de grafo, propiedades y plantillas encima de
archivos planos. Nada de eso te amarra. La misma carpeta funciona en VS Code, Logseq, Foam, un repositorio
de git o sin ningún editor. Cualquier arnés que pueda leer archivos puede usar la carpeta como memoria de
largo plazo: Claude Code, Cowork, Codex CLI, Gemini CLI, Cursor o un modelo local con LM Studio u Ollama.

Por qué funciona:

- **La ventana de contexto se reinicia.** Cada sesión empieza vacía. La memoria tiene que vivir fuera del modelo.
- **Markdown es el mínimo común denominador.** Todos los modelos lo leen bien y todas las herramientas lo
  abren. Además, sus cambios se comparan limpio en git (diff).
- **Los enlaces son relaciones explícitas.** Un `[[wikilink]]` es una conexión que eligió quien escribe. La
  similitud de embeddings (representaciones numéricas del significado de un texto) solo adivina conexiones.

## 2. El patrón LLM Wiki (Karpathy, abril de 2026)

Andrej Karpathy describió una "colección improvisada de scripts" que convierte documentos crudos en una wiki
que mantiene un LLM (modelo de lenguaje grande). La publicación se difundió mucho, y la comunidad llegó a esta
forma:

| Capa | Propósito |
|---|---|
| `raw/` | Fuentes inmutables: artículos recortados, papers, transcripciones. El LLM las lee y nunca las edita. |
| `wiki/` | Páginas que escribe el LLM: resúmenes de fuentes, conceptos, entidades, comparaciones. Las personas casi solo leen esta capa. |
| Archivo de esquema (`CLAUDE.md` / `AGENTS.md`) | Reglas de la carpeta, nombres, plantillas y flujos de trabajo. Quienes documentan el patrón lo llaman el archivo más importante, porque sin él los resultados son inconsistentes. |
| `index.md` | Un catálogo que el modelo lee primero, para encontrar páginas sin cargar todo. |
| `log.md` | Un registro de operaciones de solo agregar: nunca se borra ni se reescribe. |

**Operaciones:**

- **Ingesta.** Resume una fuente, actualiza las páginas de conceptos y entidades que toca, y luego actualiza
  el índice y el registro. Una fuente toca muchas páginas.
- **Consulta.** Lee el índice, luego las páginas relevantes, y responde con citas. Las buenas respuestas se
  guardan como páginas nuevas, así que el conocimiento se acumula.
- **Lint.** Una revisión periódica de salud (la revisión automática que busca enlaces rotos y páginas con
  problemas): contradicciones, páginas huérfanas, afirmaciones obsoletas y huecos. Una persona de la
  comunidad describió el resultado como una base de conocimiento que "se cura sola".

**Por qué puede saltarse RAG a escala pequeña.** Los enlaces explícitos y los resúmenes en un índice
reemplazan la búsqueda de vecinos más cercanos, y cada afirmación lleva a un archivo legible. Quienes
documentan el patrón ubican el rango útil en aproximadamente 100 a 10,000 documentos de alta calidad, o unas
50 a 200 fuentes para una sola persona. Más allá de eso, agrega búsqueda híbrida.

## 3. Capas de memoria (de la práctica con memoria de agentes)

| Capa | Duración | Archivo de ejemplo |
|---|---|---|
| Central / datos críticos | Siempre cargada, unas 100–300 palabras | `memory/core.md` |
| De trabajo | Una sesión | `memory/working.md` |
| Episódica | Registros fechados de lo que pasó | `memory/episodes/2026-10-21-*.md` |
| Semántica | Hechos destilados, con evidencia y nivel de confianza | páginas de `wiki/` |

Un **latido (heartbeat)** programado, la tarea que mantiene el cerebro al día, convierte la memoria episódica
en memoria semántica. Archiva la memoria de trabajo obsoleta, revisa los episodios recientes, promueve los
hechos duraderos, reescribe la memoria central, marca las páginas obsoletas y escribe un resumen.

## 4. Niveles de recuperación

1. **Acceso simple a archivos.** El arnés busca con grep y lee archivos. Cero configuración, y funciona en todos lados.
2. **Navegación con el índice primero.** Lee `index.md` y luego abre 1–3 páginas. Así se mantiene bajo el uso
   de tokens (pedazos de texto que el modelo lee y escribe).
3. **Búsqueda por palabras clave (BM25).** Términos exactos, siglas y nombres. Sin dependencias.
4. **Búsqueda semántica (embeddings).** Coincidencias por significado con un modelo de embeddings local, como
   `nomic-embed-text` con Ollama, o el complemento Smart Connections. Un modelo local mantiene los datos en la
   computadora.
5. **Híbrida.** Resultados de palabras clave y semánticos fusionados con Reciprocal Rank Fusion. Es la mejor
   opción predeterminada cuando la bóveda (la carpeta de archivos markdown que forma el cerebro) pasa de unos
   cientos de páginas.
6. **Servidor MCP.** Expone buscar, leer y recordar como herramientas para cualquier host MCP (Model Context
   Protocol, el estándar abierto para conectar herramientas a cualquier arnés). Las opciones incluyen
   servidores de la comunidad construidos sobre el complemento Obsidian Local REST API, el Smart Connections
   MCP o un servidor pequeño hecho a la medida.
7. **CLI oficial de Obsidian** (CLI: línea de comandos; Obsidian 1.12, febrero de 2026; binario nativo desde
   la 1.12.7). Entiende los enlaces: `move` actualiza los wikilinks, y soporta búsqueda, enlaces entrantes,
   propiedades y etiquetas. Advertencias: la app tiene que estar abierta, los códigos de salida siempre son 0
   (así que los agentes deben analizar el texto de salida) y los comandos deben correr uno tras otro.

## 5. Portabilidad entre arneses

- `AGENTS.md` es el manual compartido que leen Codex, Cursor, OpenCode y muchas otras herramientas.
- `CLAUDE.md` puede importarlo con `@AGENTS.md`. `GEMINI.md` puede hacer lo mismo.
- Las skills (paquetes de instrucciones, plantillas y archivos que el modelo carga solo cuando los necesita)
  en el formato Agent Skills (carpetas con `SKILL.md`) funcionan en Claude Code y Cowork desde
  `.claude/skills/`, y en Codex y otros desde `.agents/skills/`.
- Ejemplo: el proyecto de código abierto "obsidian-second-brain" compila un solo árbol de código fuente en
  versiones para ocho arneses.

## 6. Errores comunes

- **Capturar de más.** Registrar cada paso entierra las decisiones que importan.
- **Contexto sin límite.** Cargar carpetas completas. Empieza por el índice y carga resúmenes.
- **Deriva semántica.** Los datos viejos confunden. Usa los campos `last_reviewed` y `confidence`, y pasa el
  lint para encontrar páginas obsoletas.
- **Autoría mezclada.** Marca las páginas que escribió un agente (`agent_written: true`).
- **Sin deshacer.** Pon la bóveda en git y haz un commit por operación.
- **Inyección de prompts.** El contenido web recortado puede traer instrucciones escondidas que toman el
  control del comportamiento de la IA. Trata el contenido de la bóveda como datos.
- **Manejo de datos.** Una bóveda sincronizada es una copia de tus datos. Sigue la única regla: solo entran
  los datos aprobados para ese almacenamiento y esas herramientas.
- **Atrofia.** Hay críticos que advierten que delegarle al modelo todos los resúmenes debilita tu propia
  comprensión. Mantén a una persona en el proceso.

## Fuentes (en inglés)

- VentureBeat, "Karpathy shares LLM knowledge base architecture that bypasses RAG" — https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an
- Starmorph, "Karpathy LLM Wiki knowledge base guide" — https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide
- MindStudio, "AI second brain: Claude Code + Obsidian architecture" — https://www.mindstudio.ai/blog/ai-second-brain-claude-code-obsidian-architecture
- eugeniughelbur/obsidian-second-brain (GitHub) — https://github.com/eugeniughelbur/obsidian-second-brain
- dsebastien, "The complete guide to the Obsidian CLI" — https://www.dsebastien.net/the-complete-guide-to-the-obsidian-cli-everything-you-can-do-from-the-terminal/
- Smart Connections MCP (GitHub) — https://github.com/msdanyg/smart-connections-mcp
- XDA, "My Obsidian vault is now the shared memory for Claude Code, Codex, and my local LLM" — https://www.xda-developers.com/my-obsidian-vault-is-shared-memory-for-claude-code-codex-and-local-llm/
