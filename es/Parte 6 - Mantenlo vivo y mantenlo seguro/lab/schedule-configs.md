# Laboratorio 6 · Cómo programar el latido

Reemplaza `/ABSOLUTE/PATH` con tus propias rutas. Empieza con el latido (heartbeat) determinista (sin `--llm`). Agrega el
paso de reflexión solo después de revisar a mano algunas corridas.

## macOS: launchd (lo recomendado en una Mac)

Copia `brain-tools/examples/com.brain.heartbeat.plist` a `~/Library/LaunchAgents/`, edita las rutas y luego:

```bash
plutil -lint ~/Library/LaunchAgents/com.brain.heartbeat.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.brain.heartbeat.plist
launchctl kickstart gui/$(id -u)/com.brain.heartbeat     # córrela una vez ahora
launchctl bootout gui/$(id -u)/com.brain.heartbeat       # quítala otra vez
```

Comportamiento de `StartCalendarInterval`: si la Mac está **dormida** a la hora programada, launchd corre la tarea cuando
despierta, y varias horas perdidas se juntan en una sola corrida. Si la Mac está **apagada**, esa corrida se omite.

## Linux: cron

```cron
15 6 * * *  cd /ABSOLUTE/PATH/brain-vault && /ABSOLUTE/PATH/.venv/bin/brain heartbeat --commit >> .heartbeat.log 2>&1
```

cron no se pone al corriente: una corrida que se perdió mientras la máquina estaba dormida o apagada se omite.

## Windows: Programador de tareas

```bat
schtasks /create /tn BrainHeartbeat /sc daily /st 06:15 /tr "C:\brain\.venv\Scripts\brain.exe --vault C:\brain\brain-vault heartbeat --commit"
```

Para ponerte al corriente después de una corrida perdida, abre la tarea y marca **Run task as soon as possible after a scheduled start is missed** (en Windows en español: ejecutar la tarea lo antes posible si no se ejecutó a la hora programada).

## Cómo agregar el paso de reflexión de forma segura

```bash
brain heartbeat --commit --llm 'claude -p --allowedTools "Read,Edit,Write"'
```

- Permite solo herramientas de archivos. Nada de herramientas de red, correo, web ni descarga en esta sesión.
- El lint tiene que salir limpio: mientras haya caracteres ocultos o líneas que parecen inyecciones marcadas, el latido se salta el paso de reflexión.
- El paso de reflexión solo propone; nunca edita `raw/` ni `memory/core.md`. Los cambios a la memoria central llegan como `inbox/core-proposal-<date>.md`.
- `--commit` te da un commit por noche. Revísalo con `git show` y deshazlo con `git revert`.
- Revisa la documentación actual de tu herramienta para ver las opciones para correr sin interfaz (headless); cambian seguido.
