#!/usr/bin/env python3
"""verify-20260919.py — char budgets + brand-rule checks for the 2026-09-19 Northstar set."""
import re

def post_text(path):
    txt = open(path).read()
    m = re.search(r"## Post[^\n]*\n\n(.*?)\n\n---", txt, re.S)
    return m.group(1).strip()

tg = post_text("telegram-hvaccontrols-dc-aisle-containment-2026-09-19.md")
xp = post_text("x-xincahvac-dc-aisle-containment-2026-09-19.md")
li = post_text("linkedin-dc-aisle-containment-2026-09-19.md")

print("TG chars:", len(tg), "(limit 1024)  ->", "PASS" if len(tg) <= 1024 else "FAIL")
url = "help.xinca.com/a/data-center-energy-efficiency/"
weighted = len(xp) - len(url) + 23
print("X weighted chars (t.co=23):", weighted, "(limit 280)  ->", "PASS" if weighted <= 280 else "FAIL")
print("LI chars:", len(li), "(limit 3000)  ->", "PASS" if len(li) <= 3000 else "FAIL")

emoji = re.compile("[\U0001F000-\U0001FAFF\u2190-\u21FF\u2600-\u27BF\ufe0f]")
ok = True
for name, t in (("TG", tg), ("X", xp), ("LI", li)):
    hits = emoji.findall(t)
    if hits:
        ok = False
        print(name, "EMOJI FOUND:", hits)
print("emoji check:", "PASS (none)" if ok else "FAIL")

banned = ["belimo", "honeywell", "siemens", "johnson controls", "veridi", "ai-powered",
          "revolutionary", "best-in-class", "industry-leading", "coming soon"]
for name, t in (("TG", tg), ("X", xp), ("LI", li)):
    bad = [w for w in banned if w in t.lower()]
    print(name, "banned-term check:", bad or "clean")

link = "help.xinca.com/a/data-center-energy-efficiency/"
print("TG has specific link:", "PASS" if link in tg else "FAIL")
print("LI has specific link:", "PASS" if link in li else "FAIL")
print("X has specific link:", "PASS" if link in xp else "FAIL")
print("LI own-KB citations:", li.count("[XINCA Knowledge Base:"))

with open("dify-run.log", "a") as f:
    f.write("NOTE 2026-09-19: Dify app upstream provider api.xiaomimimo.com (langgenius/mimo) "
            "read-timeout at 10s on all calls incl. minimal payload and final retry - same outage "
            "as Sep 17 run. Set composed locally per documented fallback ladder.\n")
print("dify-run.log note appended")
