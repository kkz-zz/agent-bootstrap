"""Canário do scan de segredos. Roda antes do scan na CI.

Uso: python3 -I .github/scripts/canario_segredos.py <caminho do gitleaks>

Cria dois repositórios Git temporários fora do pacote:
- must-block: um commit com token no formato de PAT do GitHub, montado em tempo de
  execução (nunca versionado). O gitleaks tem que reprovar.
- must-pass: um commit sem segredo. O gitleaks tem que passar.
Se o gitleaks não reprova o token falso, o scan da CI está cego e este passo falha.
"""
import pathlib
import random
import string
import subprocess
import sys
import tempfile

gitleaks = sys.argv[1]
rng = random.SystemRandom()
fake_token = "ghp" + "_" + "".join(rng.choice(string.ascii_letters + string.digits) for _ in range(36))


def scan(content):
    with tempfile.TemporaryDirectory() as tmp:
        repo = pathlib.Path(tmp)
        git = ["git", "-C", tmp, "-c", "user.name=canario", "-c", "user.email=canario@example.com"]
        subprocess.run(git[:3] + ["init", "-q"], check=True)
        (repo / "config.txt").write_text(content, encoding="utf-8")
        subprocess.run(git + ["add", "config.txt"], check=True)
        subprocess.run(git + ["commit", "-q", "-m", "canario"], check=True)
        proc = subprocess.run([gitleaks, "git", "--redact", "--no-banner", tmp], capture_output=True, text=True)
        return proc.returncode


cases = {
    "must-block token-github": (f"token = {fake_token}\n", True),
    "must-pass  sem-segredo": ("nome = pacote de exemplo\n", False),
}
failures = []
for name, (content, should_block) in cases.items():
    code = scan(content)
    ok = (code != 0) if should_block else (code == 0)
    print(f"{name:<26} exit={code} {'ok' if ok else 'FALHOU'}")
    if not ok:
        failures.append(name)

if failures:
    print("canário de segredos falhou: o scan não se comporta como esperado em " + ", ".join(failures))
    sys.exit(1)
print("canário de segredos OK")
