---
type: source
summary: Informe de investigación de La capa de memoria, Parte 2 (el manual de operación), sobre el soporte de AGENTS.md en cada arnés, la evidencia sobre archivos de contexto, Agent Skills, las propiedades de Obsidian y la seguridad de los archivos de instrucciones.
created: 2026-10-21
---
# Informe de investigación · La capa de memoria · Parte 2: El manual de operación

**Pregunta:** ¿qué hace que todas las herramientas de IA se comporten igual dentro de un mismo cerebro, y qué dice la evidencia sobre cómo escribir ese manual?

**Respuesta corta:** un `AGENTS.md` sencillo ya es el estándar compartido. La mayoría de las herramientas lo leen directamente, y las demás se pueden apuntar a él con una línea o un ajuste. Pero la investigación sobre estos archivos da para pensar. Los recorridos largos generados automáticamente no ayudan y cuestan cerca de 20% más. Las reglas cortas, escritas por personas, sobre cosas que la IA no puede descubrir por su cuenta sí ayudan, así que eso es lo que debe contener el manual. Los procedimientos van en skills (paquetes de instrucciones, plantillas y archivos que el modelo carga solo cuando los necesita). Las plantillas y las propiedades hacen que cada página sea predecible.

---

## 1. AGENTS.md es el estándar compartido

- **Historia.** OpenAI donó AGENTS.md a la nueva **Agentic AI Foundation**, bajo la Linux Foundation, el **9 de diciembre de 2025**. La fundación se creó junto con Anthropic, que aportó MCP (Model Context Protocol, el estándar abierto para conectar herramientas a cualquier arnés), y Block, que aportó goose. En ese momento, más de **60,000** proyectos de código abierto usaban AGENTS.md. Entre las herramientas que lo soportan están Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules y VS Code. [OpenAI](https://openai.com/index/agentic-ai-foundation/)
- **Formato.** Es markdown (texto plano con formato sencillo) sin campos obligatorios. En carpetas anidadas, gana el archivo más cercano al trabajo.

### Cómo lo encuentra cada arnés (a octubre de 2026)

El arnés (en inglés, harness) es el software que rodea al modelo y decide qué puede ver y hacer.

| Arnés | ¿Lee AGENTS.md? | Detalles |
|---|---|---|
| **Codex** | De forma nativa | Arma una cadena una vez por ejecución: un `~/.codex/AGENTS.md` global (o `AGENTS.override.md`), y luego un archivo por directorio, desde la raíz del repositorio hasta la carpeta actual. Los archivos más cercanos a la carpeta actual van después y ganan. El tamaño combinado se corta en `project_doc_max_bytes`, **32 KiB** de forma predeterminada. Se pueden agregar otros nombres de archivo con `project_doc_fallback_filenames`. [Documentación de OpenAI](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| **Claude Code** | Sí, desde la v2.1.277 (18 de septiembre de 2026) | Lee AGENTS.md solo cuando **no hay CLAUDE.md** en la carpeta ni en ninguna carpeta superior. Un `CLAUDE.md` con la línea `@AGENTS.md` sigue funcionando, y es la opción más confiable. Las importaciones se anidan hasta 4 saltos. La meta es **menos de 200 líneas** por archivo, porque los archivos más largos "consumen más contexto y reducen el apego a las instrucciones". Las importaciones no reducen el costo, porque también se cargan al iniciar. El ajuste `/config` → Project instructions puede cargar ambos archivos. [Documentación de Claude Code](https://code.claude.com/docs/en/memory), [DevOps.com](https://devops.com/claude-code-adds-agents-md-fallback-cutting-instruction-file-sprawl) |
| **Gemini CLI** | Con un ajuste | Pon `"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}` en `settings.json`, o pon `@AGENTS.md` dentro de GEMINI.md. Los archivos se cargan desde un archivo global, luego desde el espacio de trabajo y sus carpetas superiores, y después justo a tiempo, conforme las herramientas abren carpetas. `/memory show` muestra lo que se cargó. [Documentación de Gemini CLI](https://www.geminicli.com/docs/cli/gemini-md) |
| **GitHub Copilot** | De forma nativa (agente de código, agosto de 2025) | Soporta archivos AGENTS.md anidados y sigue leyendo `copilot-instructions.md`, `CLAUDE.md` y `GEMINI.md`. [Changelog de GitHub](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions) |
| **Cursor, VS Code, Jules, Amp, Factory, Devin** | De forma nativa | La fundación los lista como compatibles. [OpenAI](https://openai.com/index/agentic-ai-foundation/) |
| **Apps de chat (escritorio y web)** | No por sí solas | Se conectan con un servidor MCP cuya herramienta de arranque regresa core.md y las reglas (Parte 5). |

**Punto para enseñar:** ten una sola fuente de verdad. `AGENTS.md` contiene las reglas. `CLAUDE.md` y `GEMINI.md` son punteros de una línea (`@AGENTS.md`), así que al editar un solo archivo se actualizan todas las herramientas.

## 2. La evidencia sobre archivos de contexto: menos es más

- **Evaluating AGENTS.md** (ETH Zurich, Gloaguen et al., febrero de 2026, revisado en septiembre de 2026). El estudio usó SWE-bench Lite (300 tareas) y un nuevo AGENTbench (138 tareas de 12 repositorios con archivos escritos por desarrolladores), y probó Claude Code, Codex y Qwen Code.
  - Los archivos de contexto **generados por un LLM** (modelo de lenguaje grande) *bajaron* el éxito cerca de **3%** en promedio y subieron el costo **20–23%**, con 2.5–3.9 pasos más por tarea.
  - Los archivos **escritos por desarrolladores** subieron el éxito solo cerca de **4%**, y subieron el costo hasta 19%.
  - Los agentes *sí* siguen las instrucciones; por ejemplo, una herramienta mencionada en el archivo sí se usó. Los recorridos del repositorio, que casi todos los archivos generados incluían, no ayudaron a los agentes a encontrar archivos más rápido.
  - **Recomendación:** los archivos escritos por personas deben contener solo requisitos mínimos, es decir, herramientas y prácticas que no son estándar.
  - [arXiv 2602.11988](https://arxiv.org/abs/2602.11988)
- **On the Impact of AGENTS.md Files on Efficiency** (Lulla et al., enero de 2026). En 124 PRs (pull requests) de 10 repositorios, tener AGENTS.md coincidió con un **tiempo de ejecución mediano 28.6% menor** y **16.6% menos tokens de salida** (un token es un pedazo de texto que el modelo lee y escribe), con una tasa de terminación comparable. Es una asociación, no una prueba de causa. [arXiv 2601.20404](https://arxiv.org/abs/2601.20404)
- **Do Context Files Help Coding Agents?** (Khatri, julio de 2026). El estudio hizo 288 corridas con Claude Code y Codex para comparar sin contexto, contexto siempre cargado y contexto selectivo (estilo wiki, recuperado bajo demanda).
  - Las tasas de aprobación no cambiaron de forma medible.
  - El contexto selectivo usó menos tokens de creación de caché.
  - Una sola línea que advertía que la suite completa de pruebas es lenta redujo las corridas desperdiciadas.
  - [arXiv 2607.27250](https://arxiv.org/html/2607.27250v1)
- **How Many Instructions Can LLMs Follow at Once?** (Jaroslawicz et al., julio de 2025, NeurIPS 2025). Con hasta 500 instrucciones, incluso los mejores modelos de frontera llegaron solo a **68%** de precisión en la densidad máxima. Los modelos además favorecen las instrucciones que aparecen primero (sesgo de primacía). [arXiv 2507.11538](https://arxiv.org/abs/2507.11538)
- **Síntesis práctica** (Upsun, 2026):
  - Empieza casi vacío.
  - Agrega una regla solo cuando un error se repite.
  - Incluye lo que el agente no puede descubrir; omite lo que puede leer.
  - Poda con regularidad: "Cada instrucción debe ganarse su lugar".
  - [Upsun](https://developer.upsun.com/posts/ai/agents-md-less-is-more)

**Qué significa esto para un cerebro.** Estos estudios midieron agentes de código en repositorios de código. Una bóveda de conocimiento (la bóveda es la carpeta de archivos markdown que forma el cerebro) es distinta: casi todo lo que hay en su manual es una convención que la IA *no puede* descubrir. Por ejemplo: quién puede escribir dónde, nunca editar `raw/`, el formato de las citas, cómo se manejan los conflictos y la escalera de recuperación. Ese es exactamente el tipo de contenido que la investigación encontró útil.

La lección se aplica directamente:

- escribe reglas, no un recorrido
- pon primero las reglas más importantes, por el sesgo de primacía
- quédate por debajo de unas 200 líneas
- pasa los procedimientos a skills
- prueba el manual con dos herramientas distintas

El `AGENTS.md` de la bóveda de referencia tiene 104 líneas y 5.7 KB, que son cerca de 1,400 tokens.

## 3. Skills: procedimientos que se cargan solo cuando se necesitan

- **El estándar abierto Agent Skills ([agentskills.io/specification](https://agentskills.io/specification)).** Una skill es una carpeta con un archivo `SKILL.md`, más las carpetas opcionales `scripts/`, `references/` y `assets/`.
  - **Campos obligatorios:** `name`, de máximo 64 caracteres en minúsculas y guiones, igual al nombre de la carpeta; y `description`, de máximo 1,024 caracteres, que dice qué hace la skill y cuándo usarla.
  - **Carga progresiva:** unos 100 tokens de metadatos siempre se cargan. El cuerpo, que se recomienda por debajo de 5,000 tokens y 500 líneas, se carga solo cuando se usa la skill. Los archivos referenciados se cargan solo cuando hacen falta.
  - [Espejo de la especificación](https://tangled.org/secluded.site/agent-skills/blob/a97a11da33d36feae780d2053fe504d2ce02f70c/authoring-skills/references/specification.md?raw=1)
- **Dónde busca cada herramienta:**
  - **Claude Code:** `.claude/skills/` y `~/.claude/skills/`. No lee `.agents/`. [DevOps.com](https://devops.com/claude-code-adds-agents-md-fallback-cutting-instruction-file-sprawl)
  - **Codex:** `.agents/skills/`, desde la carpeta actual hasta la raíz del repositorio, más `~/.agents/skills/` y `/etc/codex/skills/`. La lista de skills al arrancar tiene un tope de 2% de la ventana de contexto, u 8,000 caracteres. [Documentación de OpenAI](https://learn.chatgpt.com/docs/build-skills.md)
  - **Gemini CLI:** `.gemini/skills/`, con `.agents/skills/` como alias; las skills del usuario van en `~/.gemini/skills/`. Las skills del espacio de trabajo ganan. [Gemini CLI](https://geminicli.com/docs/cli/creating-skills.md)
  - **VS Code / Copilot:** `.github/skills/`, `.claude/skills/` y `.agents/skills/`, más carpetas personales. [VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- **Punto para enseñar:** guarda las skills en la carpeta `skills/` de la bóveda como fuente única. `install-skills.sh` las copia o las enlaza en `.claude/skills/` y `.agents/skills/`, que juntas cubren las cuatro familias de herramientas.
- **Las skills propias de Obsidian.** Steph Ango (kepano), CEO de Obsidian, publicó **obsidian-skills**: obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli y defuddle. Les enseñan a los agentes los formatos de archivo de la bóveda para que dejen de inventar frontmatter (el bloque de propiedades al inicio de cada página) o de romper archivos de Bases. [dsebastien.net](https://www.dsebastien.net/obsidian-ai-skills-by-steph-ango/)

## 4. Plantillas y propiedades: que cada página sea predecible

- **Las propiedades de Obsidian** son frontmatter en YAML.
  - **Tipos:** Text, List, Number, Checkbox, Date y Date & time. Un nombre tiene un solo tipo en toda la bóveda.
  - **Nombres integrados:** `tags`, `aliases` y `cssclasses`.
  - **Formato:** los enlaces dentro de las propiedades van entre comillas (`"[[page]]"`), y las fechas son `YYYY-MM-DD`.
  - No se admiten propiedades anidadas.
  - [Ayuda de Obsidian](https://huggingface.co/spaces/anpigon/obsidian-qa-bot/blob/main/docs/obsidian-help/Editing%20and%20formatting/Properties.md?code=true)
- **Bases** es un complemento central (v1.9, mayo de 2025). Convierte las propiedades en vistas vivas de tabla, tarjetas, lista, kanban o mapa, guardadas como archivos `.base`, con filtros y fórmulas. Cada consulta lee los propios archivos markdown, así que una propiedad como `last_reviewed` o `confidence` se vuelve un tablero de revisión sin código extra. [Ayuda de Obsidian](https://obsidian.md/help/bases), [changelog](https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0)
- **Plantillas:** el complemento central Templates llena `{{date}}` y `{{title}}`. La carpeta `templates/` de la bóveda tiene una plantilla por tipo de página.
- **Para qué sirve cada propiedad en la bóveda de referencia:**

| Propiedad | Quién la usa | Por qué |
|---|---|---|
| `type` | IA, Bases | Qué plantilla y qué reglas aplican |
| `summary` | IA (índice, búsqueda) | Una oración para decidir si abrir la página, sin tener que leerla para eso |
| `sources` | IA, personas | Trazabilidad; cada afirmación apunta a algún lado |
| `related` | IA, grafo | Da el siguiente peldaño de la escalera de recuperación |
| `confidence` | IA, personas | Cuánto confiar en la página; bajo significa verificar antes de apoyarse en ella |
| `created`, `updated`, `last_reviewed` | latido (heartbeat), Bases | Frescura, deriva y colas de revisión |
| `agent_written` | personas, Bases | Separa lo que escribió la IA de lo que escribieron personas; para revisión |
| `aliases` (opcional) | búsqueda, Obsidian | Los sinónimos hacen que las páginas se puedan encontrar |

## 5. Capas de memoria y su presupuesto de tokens

Estas son las capas de memoria que vimos en la Parte 1, ahora con presupuestos:

| Capa | Archivo | Se carga | Presupuesto |
|---|---|---|---|
| Reglas | `AGENTS.md` | En cada sesión | Menos de 200 líneas / unos 1–2k tokens |
| Central | `memory/core.md` | En cada sesión | 300 palabras o menos / unos 400 tokens |
| De trabajo | `memory/working.md` | En cada sesión | Unos cientos de tokens; se archiva al terminar la sesión |
| Metadatos de skills | frontmatter de `skills/*/SKILL.md` | En cada sesión | Unos 100 tokens por skill |
| Cuerpo de la skill | `SKILL.md` | Al usarla | Menos de 5k tokens |
| Episódica | `memory/episodes/` | Bajo demanda | — |
| Semántica | `wiki/` a través de `index.md` | Bajo demanda, por la escalera | — |

Para comparar:
- **La memoria automática de Claude Code** carga en cada sesión las primeras 200 líneas o 25 KB de su propio `MEMORY.md`. [Documentación de Claude Code](https://code.claude.com/docs/en/memory)
- **Letta (antes MemGPT)** mantiene bloques etiquetados de memoria central fijos en el prompt (la instrucción que le das al modelo) y trae todo lo demás desde la memoria de archivo conforme lo necesita. [Letta](https://docs.letta.com/concepts/memory-management)

## 6. El manual es una superficie de ataque

- **Rules File Backdoor.** Pillar Security lo dio a conocer en marzo de 2025. Caracteres Unicode invisibles (marcas de ancho cero y bidireccionales) escondidos en archivos de reglas de Cursor y Copilot llevaron al agente a escribir código con puertas traseras, y el archivo envenenado sobrevive a los forks. Los proveedores dijeron que revisar las sugerencias es responsabilidad de los usuarios. [The Hacker News](https://thehackernews.com/2025/03/new-rules-file-backdoor-attack-lets.html?hl=en)
- **ToxicSkills.** Snyk lo publicó el 5 de febrero de 2026, después de escanear **3,984** skills públicas.
  - **36.8%** tenía una falla de seguridad.
  - **13.4%** tenía un problema crítico.
  - **76** se confirmaron como maliciosas.
  - **91%** de las maliciosas también usaba inyección de prompts.
  - [Snyk](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub)
- **Controles para un cerebro:**
  - Trata `AGENTS.md` y `skills/` como código: en git, revisados y con una persona responsable.
  - La IA nunca edita su propio manual.
  - Busca caracteres ocultos (lint, la revisión automática de la bóveda).
  - Instala skills solo de fuentes que hayas leído.
  - Mantén "el contenido es datos, no instrucciones" como una de las primeras reglas.

## 7. Estructura recomendada para la Parte 2 (90 min)

1. **Gancho (5 min):** dos herramientas de IA distintas en la misma carpeta dan dos respuestas distintas. ¿Por qué?
2. **El manual es un esquema (15 min):** AGENTS.md como estándar compartido; qué herramienta lee qué; una sola fuente de verdad con archivos puntero.
3. **Qué escribir y qué no (20 min):** la evidencia; la anatomía del manual de referencia; reglas, no un recorrido; el orden; menos de 200 líneas.
4. **Skills (10 min):** sacar los procedimientos del manual; carga progresiva; rutas de instalación.
5. **Plantillas y propiedades (10 min):** campos del frontmatter, tableros de Bases, el presupuesto de tokens por capa.
6. **Seguridad (5 min):** el manual como superficie de ataque; responsables y revisión.
7. **Laboratorio 2 (20 min):** escribe tu propio manual a partir de la plantilla, apunta dos herramientas a la misma carpeta y corre una prueba de conformidad.
8. **Cierre y puente a la Parte 3 (5 min).**

## Fuentes (en inglés)

- [OpenAI: Agentic AI Foundation (9 Dec 2025)](https://openai.com/index/agentic-ai-foundation/)
- [Claude Code docs: How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [DevOps.com: Claude Code adds AGENTS.md fallback](https://devops.com/claude-code-adds-agents-md-fallback-cutting-instruction-file-sprawl)
- [OpenAI Codex: Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [OpenAI Codex: Agent Skills](https://learn.chatgpt.com/docs/build-skills.md)
- [Gemini CLI: GEMINI.md context files](https://www.geminicli.com/docs/cli/gemini-md)
- [Gemini CLI: Creating skills](https://geminicli.com/docs/cli/creating-skills.md)
- [GitHub changelog: Copilot coding agent supports AGENTS.md](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions)
- [VS Code: Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [Gloaguen et al., Evaluating AGENTS.md (arXiv 2602.11988)](https://arxiv.org/abs/2602.11988)
- [Lulla et al., Impact of AGENTS.md on efficiency (arXiv 2601.20404)](https://arxiv.org/abs/2601.20404)
- [Khatri, Do Context Files Help Coding Agents? (arXiv 2607.27250)](https://arxiv.org/html/2607.27250v1)
- [Jaroslawicz et al., How Many Instructions Can LLMs Follow at Once? (arXiv 2507.11538)](https://arxiv.org/abs/2507.11538)
- [Upsun: your AGENTS.md is probably too long](https://developer.upsun.com/posts/ai/agents-md-less-is-more)
- [Obsidian help: Bases](https://obsidian.md/help/bases)
- [Obsidian help: Properties](https://huggingface.co/spaces/anpigon/obsidian-qa-bot/blob/main/docs/obsidian-help/Editing%20and%20formatting/Properties.md?code=true)
- [dsebastien.net: Obsidian AI skills by Steph Ango](https://www.dsebastien.net/obsidian-ai-skills-by-steph-ango/)
- [Snyk: ToxicSkills (5 Feb 2026)](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub)
- [The Hacker News: Rules File Backdoor (18 Mar 2025)](https://thehackernews.com/2025/03/new-rules-file-backdoor-attack-lets.html?hl=en)
- [Letta: memory management](https://docs.letta.com/concepts/memory-management)
