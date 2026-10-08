"""Gate check-docs: consistência interna dos arquivos Markdown do pacote.

Uso: python3 -I .github/scripts/check_docs.py <raiz>

Regras (o código entre colchetes aparece em cada erro e é o que os canários cobrem):
  [link]     link relativo aponta para arquivo que não existe
  [ancora]   link para âncora que não existe no arquivo de destino
  [pergunta] ID de pergunta da entrevista (A1, E4a, H8…) citado e não definido
  [modulo]   ID de módulo fora do catálogo M1–M15

A pasta .github não é escaneada: ela guarda os canários, que quebram as regras de propósito.
Saída diferente de zero quando há erro. Cada linha diz arquivo, regra e o que fazer.
"""
import pathlib
import re
import sys

RULES = ("link", "ancora", "pergunta", "modulo")
MODULE_MAX = 15

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
files = sorted(p for p in root.rglob("*.md") if not {".git", ".github"} & set(p.relative_to(root).parts))
errors = []


def slug(heading):
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    return heading.replace(" ", "-")


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


texts = {p: p.read_text(encoding="utf-8") for p in files}
anchors = {p: {slug(m.group(1)) for m in re.finditer(r"^#+\s+(.*)$", t, re.M)} for p, t in texts.items()}
questions = {m.group(1) for t in texts.values() for m in re.finditer(r"^- \*\*([A-H]\d+a?)\.\*\*", t, re.M)}


def report(path, rule, detail, fix):
    errors.append(f"{path.relative_to(root)}: [{rule}] {detail} — {fix}")


for path, text in texts.items():
    prose = strip_code(text)
    for m in re.finditer(r"\]\(([^)\s]+)\)", prose):
        target = m.group(1)
        if re.match(r"^[a-z]+:", target):
            continue
        file_part, _, frag = target.partition("#")
        dest = (path.parent / file_part).resolve() if file_part else path
        if file_part and not dest.exists():
            report(path, "link", f"{target} não existe", "corrija o caminho ou crie o arquivo")
        elif frag and dest.suffix == ".md" and frag not in anchors.get(dest, set()) and not frag.endswith("-ov-file"):
            report(path, "ancora", f"#{frag} não existe em {dest.name}", "use o slug do título de destino")
    for m in re.finditer(r"(?<![\w-])([A-H]\d+a?)(?![\w-])", prose):
        if m.group(1) not in questions:
            report(path, "pergunta", f"{m.group(1)} citada e não definida", "defina no bloco da entrevista ou corrija o ID")
    for m in re.finditer(r"(?<![\w-])M(\d+)(?![\w-])", prose):
        if not 1 <= int(m.group(1)) <= MODULE_MAX:
            report(path, "modulo", f"M{m.group(1)} fora de M1–M{MODULE_MAX}", "use um ID do catálogo em AGENT-BOOTSTRAP.md §3")

print(f"check-docs: {len(files)} arquivos, {len(questions)} perguntas definidas")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
