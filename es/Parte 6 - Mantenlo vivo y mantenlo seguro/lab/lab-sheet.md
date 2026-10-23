# Laboratorio 6 · Guía del laboratorio

Usa una copia de tu bóveda que sea un repositorio git. Si solo tienes la bóveda de referencia:

```bash
cp -R brain-vault ~/brain-copy && cd ~/brain-copy && git init -q && git add -A && git commit -qm baseline
export BRAIN_VAULT=~/brain-copy
```

## A. Corre el latido una vez a mano (4 min)

```bash
brain heartbeat --commit
git log --oneline -2 && git show --stat HEAD
```

1. ¿Qué archivos cambió el latido (heartbeat)? ______________________________
2. Abre `memory/reports/<today>.md`. ¿Cuántos problemas encontró el lint? ______

## B. Ponlo en un horario (5 min)

Elige tu sistema operativo en `schedule-configs.md`. Carga la tarea y luego córrela una vez ahora (`launchctl kickstart …` en una Mac).

3. Tu Mac está dormida a las 6:17 a. m. y abres la tapa a las 7:40 a. m. ¿Qué pasa con launchd? ¿Y con cron?
   ______________________________
4. La laptop estaba **apagada** a las 6:17 a. m. ¿Qué pasa? ______________________________

## C. Planta dos recortes maliciosos (5 min)

```bash
cp lab/planted-clip.md lab/invisible-ink.md "$BRAIN_VAULT/inbox/"
brain lint
brain heartbeat --commit --llm "echo reflect"
tail -1 "$BRAIN_VAULT/log.md"
```

5. ¿Qué línea marcó el lint en cada archivo? ______________________________
6. Abre `invisible-ink.md` en tu editor. ¿Puedes ver la instrucción escondida? ______
7. ¿Corrió el paso de reflexión? ¿Por qué sí o por qué no? ______________________________

Atajo: `python3 lab/lab6_check.py ~/brain-copy` hace los pasos C y D en una copia temporal e imprime el resultado.

## D. Revisa como persona (4 min)

8. Borra los dos recortes (son ataques, no fuentes) y vuelve a correr `brain heartbeat --commit --llm "echo reflect"`.
   ¿Esta vez sí corrió el paso de reflexión? ______
9. Elige una página de la wiki. Agrega `review_after:` con una fecha pasada y corre `brain lint`. ¿Qué sección la menciona? ______
10. Lee `git show HEAD`. Nombra un cambio que rechazarías, o escribe "ninguno". ______________________________

## E. Tu regla (2 min)

11. Escribe la oración que pondrías en tu propio `AGENTS.md` sobre lo que la corrida nocturna puede cambiar y lo que no.
    ______________________________
