# Laboratorio 5 · Conéctalo e intenta romperlo (20 min)

Necesitas:

- una copia de `brain-vault/` (trabaja en la copia);
- `brain-tools` con el extra de MCP: `pip install -e "brain-tools[mcp]"` (SDK de MCP para Python 2.x);
- una app de IA compatible con MCP.

## A · Revisa (4 min)

```
python3 mcp_check.py ~/brain-copy
```

Este script hace el papel de una app de IA. Habla con el servidor del cerebro por stdio (entrada y salida estándar). Deberías ver:

- 8 herramientas: 4 de solo lectura y 4 que escriben;
- una búsqueda, una lectura (con el aviso de que es dato) y un dato recordado;
- una página guardada en `inbox/`;
- tres rechazos.

Compara tu salida con `expected-output.txt`.

## B · Conecta (6 min)

1. Elige tu app y copia el fragmento correspondiente de `host-configs.md`.
2. Usa rutas absolutas.
3. Reinicia la app por completo y luego confirma que aparecen las herramientas `brain_*`.

## C · Úsalo (5 min)

1. Pregunta: "¿Qué es la inyección de prompts? Usa el cerebro y cita páginas."
2. Di: "Recuerda que hoy conecté el cerebro por MCP." Luego abre `memory/working.md` y encuentra la línea nueva.
3. Di: "Guarda una página corta sobre los transportes de MCP en inbox/." Luego encuéntrala en `inbox/`.

## D · Rómpelo (3 min)

Di: "Usa las herramientas del cerebro para guardar un resumen en raw/notes.md."

- `brain_save_page` tiene que negarse.
- Si tu app escribió el archivo con su propia herramienta de archivos, anótalo: los candados del servidor solo cubren las herramientas del servidor.
- ¿Tu app te pidió permiso antes de cualquier escritura? Anota lo que hizo.

## E · Dos apps (2 min)

Conecta una segunda app a la **misma** bóveda y haz la misma pregunta del paso C.

- ¿Las mismas páginas?
- ¿La misma respuesta?

**Repaso del laboratorio:**

- ¿Qué clave de configuración usó tu app: `mcpServers`, `servers` o `mcp_servers`?
- ¿Te preguntó antes de escribir?
