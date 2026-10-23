"""Lab 6 check: plant two bad clippings in a COPY of a vault, then run lint and the heartbeat.

Usage:  python3 lab6_check.py <path to brain-vault>
Needs brain-tools installed (pip install -e brain-tools). Never touches the vault you pass in.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
work = Path(tempfile.mkdtemp(prefix="lab6-")) / "vault"
shutil.copytree(src, work, ignore=shutil.ignore_patterns(".brain", ".git", ".obsidian"))
print(f"copy: {work}")

def brain(*args):
    p = subprocess.run(["brain", "--vault", str(work), "--json", *args], capture_output=True, text=True)
    return json.loads(p.stdout) if p.stdout.strip().startswith("{") else p.stdout

def git(*args):
    return subprocess.run(["git", *args], cwd=work, capture_output=True, text=True)

git("init", "-q"); git("add", "-A")
git("-c", "user.name=lab", "-c", "user.email=lab@example.com", "commit", "-qm", "baseline")

print("\n1) clean vault")
r = brain("lint")
print(f"   lint issues: {r['issue_count']}")

print("\n2) plant two clippings in inbox/")
(work / "inbox").mkdir(exist_ok=True)
for name in ("planted-clip.md", "invisible-ink.md"):
    shutil.copy(HERE / name, work / "inbox" / name)
    print(f"   + inbox/{name}")
git("add", "-A"); git("-c", "user.name=lab", "-c", "user.email=lab@example.com", "commit", "-qm", "plant clippings")

r = brain("lint")["issues"]
for kind in ("hidden_characters", "injection_suspects"):
    for it in r[kind]:
        print(f"   {kind}: {it['path']}:{it['line']}" + (f"  ({it.get('char') or it.get('text')})"))

print("\n3) heartbeat with a reflect step")
out = brain("heartbeat", "--no-embed", "--commit", "--llm", "echo reflect")
print(f"   reflect: {out.get('llm')}")
print(f"   quarantined: {out.get('quarantined')}")
print(f"   commit: {out.get('commit')}")
print("   log: …" + (work / "log.md").read_text(encoding="utf-8").strip().splitlines()[-1][-62:])

print("\n4) a person reviews the clippings and removes them")
for name in ("planted-clip.md", "invisible-ink.md"):
    (work / "inbox" / name).unlink()
git("add", "-A"); git("-c", "user.name=lab", "-c", "user.email=lab@example.com", "commit", "-qm", "remove bad clippings")
out = brain("heartbeat", "--no-embed", "--commit", "--llm", "echo reflect")
print(f"   reflect: {out.get('llm', {}).get('cmd')} (returncode {out.get('llm', {}).get('returncode')})")
print(f"   commit: {out.get('commit')}")
print("\n" + git("log", "--oneline").stdout.strip())
