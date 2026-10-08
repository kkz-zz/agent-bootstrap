"""Canários do gate check-docs. Rodam antes do gate na CI.

- must-pass/<caso>/: o gate tem que sair com 0.
- must-block/<regra>/: o gate tem que sair diferente de 0 e reportar só [<regra>].
- Cobertura: toda regra listada em RULES no gate tem um caso must-block, e todo caso
  must-block corresponde a uma regra. Regra nova sem canário reprova aqui.
"""
import pathlib
import re
import subprocess
import sys

here = pathlib.Path(__file__).resolve().parent
gate = here / "check_docs.py"
cases = here.parent / "canarios" / "check-docs"

rules = set(re.search(r"^RULES = \(([^)]*)\)", gate.read_text(encoding="utf-8"), re.M).group(1).replace('"', "").replace(" ", "").strip(",").split(","))
failures = []


def run(case):
    proc = subprocess.run([sys.executable, "-I", str(gate), str(case)], capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


for case in sorted((cases / "must-pass").iterdir()):
    code, out = run(case)
    status = "ok" if code == 0 else "FALHOU"
    print(f"must-pass  {case.name:<10} exit={code} {status}")
    if code != 0:
        failures.append(f"must-pass/{case.name} reprovou:\n{out}")

blocked = set()
for case in sorted((cases / "must-block").iterdir()):
    blocked.add(case.name)
    code, out = run(case)
    found = set(re.findall(r"\[(\w+)\]", out))
    ok = code != 0 and found == {case.name}
    print(f"must-block {case.name:<10} exit={code} regras={sorted(found)} {'ok' if ok else 'FALHOU'}")
    if not ok:
        failures.append(f"must-block/{case.name} esperava só [{case.name}] e saída != 0:\n{out}")

if rules != blocked:
    failures.append(f"cobertura: regras sem canário {sorted(rules - blocked)}, canários sem regra {sorted(blocked - rules)}")
print(f"cobertura  regras={sorted(rules)} canários={sorted(blocked)}")

if failures:
    print("\n".join(failures))
    sys.exit(1)
print("canários OK")
