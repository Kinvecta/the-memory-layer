# Temario

La capa de memoria es un curso de seis partes para construir un "segundo cerebro" para tu IA: archivos simples y enlazados en markdown (texto plano con formato sencillo) que cualquier herramienta de IA puede leer, buscar, citar y mantener al día. Cada parte es un video corto con diapositivas, un laboratorio práctico con clave de respuestas, un informe de investigación con fuentes y una transcripción.

Toma las partes en orden. Cada laboratorio parte de la bóveda (la carpeta de archivos markdown que forma el cerebro) del anterior. Necesitas Python 3.10+, git y cualquier herramienta de IA para programar o app de chat. La bóveda de referencia en [`brain-vault/`](../../brain-vault/) y las herramientas en [`brain-tools/`](../../brain-tools/) son el resultado terminado, para que compares el tuyo.

| Parte | Título | Lo que vas a aprender | Materiales |
|:--:|---|---|---|
| 1 | [Por qué tu IA necesita un cerebro](../Parte%201%20-%20Por%20qu%C3%A9%20tu%20IA%20necesita%20un%20cerebro/) | Por qué la IA olvida, tres formas de darle memoria y el patrón LLM Wiki: una carpeta de páginas enlazadas en markdown que la IA mantiene por ti. | [video](https://youtu.be/WAMMWuCq_tA) · [diapositivas](../Parte%201%20-%20Por%20qu%C3%A9%20tu%20IA%20necesita%20un%20cerebro/diapositivas.pdf) · [laboratorio](../Parte%201%20-%20Por%20qu%C3%A9%20tu%20IA%20necesita%20un%20cerebro/lab/) · [informe](../Parte%201%20-%20Por%20qu%C3%A9%20tu%20IA%20necesita%20un%20cerebro/informe-de-investigacion.md) |
| 2 | [El manual de operación](../Parte%202%20-%20El%20manual%20de%20operaci%C3%B3n/) | Un solo AGENTS.md que lee cualquier herramienta de IA; plantillas, capas de memoria y una prueba de conformidad. | [video](https://youtu.be/Qs9PkI2loZY) · [diapositivas](../Parte%202%20-%20El%20manual%20de%20operaci%C3%B3n/diapositivas.pdf) · [laboratorio](../Parte%202%20-%20El%20manual%20de%20operaci%C3%B3n/lab/) · [informe](../Parte%202%20-%20El%20manual%20de%20operaci%C3%B3n/informe-de-investigacion.md) |
| 3 | [Ingesta, consulta y lint](../Parte%203%20-%20Ingesta,%20consulta%20y%20lint/) | Haz que el conocimiento se acumule: incorpora fuentes a la wiki, responde con citas, pasa el lint para encontrar problemas y revierte una página envenenada. | [video](https://youtu.be/1AbY72w_w4E) · [diapositivas](../Parte%203%20-%20Ingesta,%20consulta%20y%20lint/diapositivas.pdf) · [laboratorio](../Parte%203%20-%20Ingesta,%20consulta%20y%20lint/lab/) · [informe](../Parte%203%20-%20Ingesta,%20consulta%20y%20lint/informe-de-investigacion.md) |
| 4 | [Recuperación a escala](../Parte%204%20-%20Recuperaci%C3%B3n%20a%20escala/) | Búsqueda híbrida: BM25 más embeddings locales, fusionados con RRF y medidos con recall@5 y MRR sobre un conjunto de referencia. | [video](https://youtu.be/k_lTdCUlF0c) · [diapositivas](../Parte%204%20-%20Recuperaci%C3%B3n%20a%20escala/diapositivas.pdf) · [laboratorio](../Parte%204%20-%20Recuperaci%C3%B3n%20a%20escala/lab/) · [informe](../Parte%204%20-%20Recuperaci%C3%B3n%20a%20escala/informe-de-investigacion.md) |
| 5 | [Conéctalo donde sea](../Parte%205%20-%20Con%C3%A9ctalo%20donde%20sea/) | Un servidor MCP para todas las apps de IA: transportes, configuraciones del host y barreras de seguridad para las escrituras. | [video](https://youtu.be/t-3wWGLiYBI) · [diapositivas](../Parte%205%20-%20Con%C3%A9ctalo%20donde%20sea/diapositivas.pdf) · [laboratorio](../Parte%205%20-%20Con%C3%A9ctalo%20donde%20sea/lab/) · [informe](../Parte%205%20-%20Con%C3%A9ctalo%20donde%20sea/informe-de-investigacion.md) |
| 6 | [Mantenlo vivo y mantenlo seguro](../Parte%206%20-%20Mantenlo%20vivo%20y%20mantenlo%20seguro/) | Un latido (heartbeat) programado que solo propone, fechas de caducidad para las páginas y cuarentena para notas con inyección de prompts o tinta invisible. | [video](https://youtu.be/AxG7RSe7w8U) · [diapositivas](../Parte%206%20-%20Mantenlo%20vivo%20y%20mantenlo%20seguro/diapositivas.pdf) · [laboratorio](../Parte%206%20-%20Mantenlo%20vivo%20y%20mantenlo%20seguro/lab/) · [informe](../Parte%206%20-%20Mantenlo%20vivo%20y%20mantenlo%20seguro/informe-de-investigacion.md) |

## Al terminar, podrás

- Explicar por qué la memoria del chat y la simple recuperación no bastan, y mantener un cerebro como markdown enlazado que es tuyo.
- Escribir un solo manual de operación, `AGENTS.md`, que siga cualquier herramienta de IA.
- Incorporar fuentes, responder con citas y revisar la bóveda con lint (la revisión automática que busca enlaces rotos y páginas con problemas) para encontrar páginas rotas, obsoletas o envenenadas.
- Buscar en el cerebro con recuperación híbrida, BM25 (búsqueda por palabras clave con puntaje) + embeddings (representaciones numéricas del significado de un texto), y medir la recuperación.
- Servir el cerebro a cualquier app de IA por MCP (Model Context Protocol, el estándar abierto para conectar herramientas a cualquier app de IA) con límites de escritura seguros.
- Mantenerlo al día con un latido programado que solo propone, y protegerlo contra la inyección de prompts (instrucciones escondidas en un contenido que toman el control del comportamiento de la IA) y la filtración de secretos.

La lista de reproducción es [La capa de memoria: construye un segundo cerebro para tu IA (en español)](https://www.youtube.com/playlist?list=PLBx8rYlb7T2Y).

English version: [`course/`](../../course/)
