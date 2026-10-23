# Laboratorio 5 · Agrega el cerebro a tu app de IA

Reemplaza `/ABSOLUTE/PATH` con tus rutas reales:

- `brain-mcp` vive en el entorno virtual donde instalaste `brain-tools`, por ejemplo `brain-tools/.venv/bin/brain-mcp`.
- Usa la ruta completa. Muchas apps no cargan el PATH de tu shell.

Después de editar una configuración, **cierra la app por completo y vuelve a abrirla**, y luego revisa que aparezcan las herramientas `brain_*`.

## La mayoría de las apps: `mcpServers` (JSON)

Úsalo en un `.mcp.json` de proyecto, en el archivo de configuración de una app de chat de escritorio, en Cursor (`.cursor/mcp.json`), en Gemini CLI (`settings.json`) y en LM Studio (`mcp.json`):

```json
{
  "mcpServers": {
    "brain": {
      "command": "/ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp",
      "env": { "BRAIN_VAULT": "/ABSOLUTE/PATH/brain-vault" }
    }
  }
}
```

Ejemplos de comandos para agregarlo (revisa la documentación de tu app):

```
claude mcp add brain -e BRAIN_VAULT=/ABSOLUTE/PATH/brain-vault -- /ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp
gemini mcp add -e BRAIN_VAULT=/ABSOLUTE/PATH/brain-vault brain /ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp
```

## IDEs que usan `servers` (JSON), por ejemplo `.vscode/mcp.json` en VS Code

```json
{
  "servers": {
    "brain": {
      "type": "stdio",
      "command": "/ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp",
      "env": { "BRAIN_VAULT": "/ABSOLUTE/PATH/brain-vault" }
    }
  }
}
```

## CLIs que usan TOML, por ejemplo `~/.codex/config.toml` en Codex

```toml
[mcp_servers.brain]
command = "/ABSOLUTE/PATH/brain-tools/.venv/bin/brain-mcp"

[mcp_servers.brain.env]
BRAIN_VAULT = "/ABSOLUTE/PATH/brain-vault"
```

## Compartir un cerebro por HTTP (avanzado; no se necesita para el laboratorio)

```
brain serve --http --port 8765      # sirve http://127.0.0.1:8765/mcp, solo en localhost
```

El servidor rechaza las solicitudes que vienen de otros orígenes web (HTTP 403), pero **no tiene inicio de sesión**. Compártelo solo detrás de un proxy inverso que agregue autenticación.

## Solución de problemas

- **No aparecen las herramientas.** La ruta está mal o la app no se reinició. Corre el comando en una terminal: debería imprimir una línea `vault: …` y luego quedarse esperando. Presiona Ctrl-C para detenerlo.
- **"No module named mcp".** Instala el extra: `pip install -e "brain-tools[mcp]"`.
- **La búsqueda no encuentra nada.** Primero corre `brain index` en la bóveda.
