#!/usr/bin/env python3
"""Change detector. For each topic fetch the official source URL and confirm every
'check' string (the key values we publish) still appears in it. Exit 1 and print a
report if any value is missing (= source changed or fetch failed -> agent must review manually).
Run on a schedule; on drift, the agent reads the source, updates data/data.json (values,
effective date, checked date, add a 'changes' entry), runs build.py, commits."""
import json, sys, urllib.request, pathlib, re, datetime
root = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((root/"data/data.json").read_text(encoding="utf-8"))
def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0 (rates-tracker check)"})
    return urllib.request.urlopen(req, timeout=40).read()
def text(b, u):
    if u.lower().endswith(".pdf"):
        import subprocess, tempfile
        f = tempfile.NamedTemporaryFile(suffix=".pdf"); f.write(b); f.flush()
        return subprocess.run(["pdftotext", f.name, "-"], capture_output=True).stdout.decode("utf-8","ignore")
    return b.decode("utf-8","ignore")
def norm(s): return re.sub(r"[,\s]", "", s)
bad = []
today = datetime.date.today().isoformat()
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
def adapter_check(t):
    """Topics with an adapter: compare stored expect values against the live official API."""
    import update as U
    at = t["adapter"]; exp = at.get("expect", {})
    if at["type"] == "cbs_cpi":
        st = U.fetch_cpi()
        got = {"period": f"{st['year']}-{st['month']:02d}", "level": f"{st['value']:g}", "mom": f"{st['mom']:g}", "yoy": f"{st['yoy']:g}"}
    elif at["type"] == "boi_interest":
        st = U.fetch_boi()
        got = {"rate": f"{st['rate']:g}", "next": st["next"], "published": st["published"]}
    else:
        return ["unknown adapter type " + str(at.get("type"))]
    return [f"adapter {k}: published '{exp.get(k)}' != live '{v}'" for k, v in got.items() if str(exp.get(k)) != str(v)]

for t in D["topics"]:
    u = t["source"]["url"]
    nr = t.get("next_review")
    if nr and today >= nr:  # live topic: a new release is due or out; agent must refresh value, dates, changes entry
        bad.append((t["slug"], f"DUE: new release expected since {nr} - refresh from {u}"))
    if t.get("adapter"):
        try:
            for m in adapter_check(t): bad.append((t["slug"], m))
        except Exception as ex: bad.append((t["slug"], f"ADAPTER FETCH FAILED: {ex}")); continue
    if t.get("adapter"): continue  # adapter topics are verified against the API, not string-matched
    if t.get("check_mode") == "due": continue  # source page not fetchable by script (JS/403): due-date only
    try: body = norm(text(fetch(u), u))
    except Exception as ex: bad.append((t["slug"], f"FETCH FAILED: {ex}")); continue
    for c in t["check"]:
        if norm(c) not in body: bad.append((t["slug"], f"value '{c}' not found at {u}"))
print(datetime.date.today(), "drift:" if bad else "all values match sources")
for s, m in bad: print(" -", s, m)
sys.exit(1 if bad else 0)
