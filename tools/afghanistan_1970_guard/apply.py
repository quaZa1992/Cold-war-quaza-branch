"""Stop the 2000-era Taliban insurgency and its border-war decisions from running in the 1970 scenario."""
import re, sys, os
src, dst = sys.argv[1], sys.argv[2]
G = "NOT = { IMP_is_1970_scenario = yes } # COLDWAR: border wars crash the 1970 scenario"

def write(rel, text):
    p = os.path.join(dst, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(text)

# 1) the insurgency start event
rel = "events/Afghanistan.txt"
t = open(os.path.join(src, rel), encoding="utf-8").read()
old = "\tid = AFG_taliban_insurgency.0\n\ttitle = AFG_taliban_insurgency.0.t\n\tdesc = AFG_taliban_insurgency.0.d\n\tpicture = GFX_taliban_insurgency_start\n\tis_triggered_only = yes\n"
if "no Taliban insurgency in the 1970" not in t:
    assert t.count(old) == 1
    t = t.replace(old, old + "\t# COLDWAR: no Taliban insurgency in the 1970 scenario (its border wars crash the game)\n\ttrigger = { NOT = { IMP_is_1970_scenario = yes } }\n")
write(rel, t)

# 2) every decision that starts a border war
rel = "common/decisions/05_afghanistan.txt"
t = open(os.path.join(src, rel), encoding="utf-8").read()
out, i, n = [], 0, 0
for m in re.finditer(r"\n\t(\w+) = \{\n", t):
    pass
pos = 0
pattern = re.compile(r"\n\t(\w+) = \{\n")
res = []
last = 0
for m in pattern.finditer(t):
    start = m.start() + 1
    d = 0
    for k in range(m.end() - 2, len(t)):
        if t[k] == "{": d += 1
        elif t[k] == "}":
            d -= 1
            if d == 0: break
    block = t[start:k + 1]
    if "start_border_war" in block and G not in block:
        if "\n\t\tvisible = {\n" in block:
            block = block.replace("\n\t\tvisible = {\n", f"\n\t\tvisible = {{\n\t\t\t{G}\n", 1)
        elif re.search(r"\n\t\tvisible = \{", block):
            block = re.sub(r"\n\t\tvisible = \{", f"\n\t\tvisible = {{ {G}", block, count=1)
        else:
            block = block.replace(" = {\n", f" = {{\n\t\tvisible = {{ {G} }}\n", 1)
        n += 1
    res.append(t[last:start]); res.append(block); last = k + 1
res.append(t[last:])
t2 = "".join(res)
write(rel, t2)
print("guarded decisions:", n)
