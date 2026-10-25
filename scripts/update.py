#!/usr/bin/env python3
"""Autonomous data updater. For topics carrying an 'adapter' block in data/data.json,
fetch the official API, validate, and update values/dates/changes feed in place.
--dry-run (default): print the planned changes, write nothing.
--apply: write data.json. Exit 1 if any adapter fails validation -> the workflow
opens a GitHub issue and fails (email -> agent verification). Never guesses values."""
import json, sys, urllib.request, pathlib, datetime

root = pathlib.Path(__file__).resolve().parent.parent
P = root / "data/data.json"
UA = {"User-Agent": "Mozilla/5.0 (rates-tracker update)"}
CBS = "https://api.cbs.gov.il/index/data/price?id={id}&format=json&download=false&last=1"
BOI = "https://www.boi.org.il/PublicApi/GetInterest"
CBS_API_SRC = "https://api.cbs.gov.il/index/data/price?id=120010&format=json"
MONTHS = {1:"ינואר",2:"פברואר",3:"מרץ",4:"אפריל",5:"מאי",6:"יוני",7:"יולי",8:"אוגוסט",9:"ספטמבר",10:"אוקטובר",11:"נובמבר",12:"דצמבר"}

def get_json(u):
    req = urllib.request.Request(u, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=40).read())

def today(): return datetime.date.today().isoformat()

def direction(pct):
    return "עלייה" if pct > 0 else ("ירידה" if pct < 0 else "ללא שינוי")

def next15(y, m, skip=1):
    # period month m publishes on the 15th of month m+1; next review is the 15th of month m+1+skip-... i.e. m+2
    m2 = (m + skip - 1) % 12 + 1
    y2 = y + ((m + skip - 1) // 12)
    return y2, m2

def fetch_cpi():
    d = get_json(CBS.format(id=120010))
    e = d["month"][0]["date"][0]
    y, m = int(e["year"]), int(e["month"])
    val, mom, yoy = float(e["currBase"]["value"]), float(e["percent"]), float(e["percentYear"])
    # validation gates
    assert 50 <= val <= 250, f"CPI level out of range: {val}"
    assert abs(mom) <= 5, f"CPI MoM out of range: {mom}"
    assert abs(yoy) <= 15, f"CPI YoY out of range: {yoy}"
    assert 2020 <= y <= 2100 and 1 <= m <= 12, f"CPI period implausible: {y}-{m}"
    return {"year": y, "month": m, "value": val, "mom": mom, "yoy": yoy}

def fetch_boi():
    d = get_json(BOI)
    rate = float(d["currentInterest"])
    nxt = d["nextInterestDate"][:10]
    pub = d["lastPublishedDate"][:10]
    assert 0 <= rate <= 25, f"BoI rate out of range: {rate}"
    assert abs(rate * 4 - round(rate * 4)) < 1e-9, f"BoI rate not a 0.25 step: {rate}"
    datetime.date.fromisoformat(nxt); datetime.date.fromisoformat(pub)
    return {"rate": rate, "next": nxt, "published": pub}

def fmt_pct(x):
    s = f"{abs(x):g}"
    return s

def upd_cpi(t, st, changes):
    y, m = st["year"], st["month"]
    period = f"{y}-{m:02d}"
    a = t.setdefault("adapter", {"type": "cbs_cpi"})
    if a.get("expect", {}).get("period") == period:
        t["checked"] = today()
        return False  # already current; refresh check date only
    prev = (y, m - 1) if m > 1 else (y - 1, 12)
    mon = f"{MONTHS[m]} {y}"
    d = direction(st["mom"])
    pct = fmt_pct(st["mom"])
    # content rewrite
    t["title"] = f"מדד המחירים לצרכן {mon}: {d}" + (f" של {pct}%" if st["mom"] != 0 else "")
    row = [mon, f"{st['value']:g}", f"{d} של {pct}%" if st["mom"] != 0 else "ללא שינוי"]
    t["table"]["rows"] = ([row] + t["table"]["rows"])[:3]
    for f in t.get("facts", []):
        if f[0].startswith("שינוי ב-12"):
            f[0] = f"שינוי ב-12 החודשים האחרונים ({mon} לעומת {MONTHS[m]} {y-1})"
            f[1] = f"{direction(st['yoy'])} של {fmt_pct(st['yoy'])}%" if st["yoy"] != 0 else "ללא שינוי"
        elif f[0].startswith("המדד הבא"):
            ny, nm = next15(y, m, skip=2)   # next index is month m+1, published 15th of month m+2
            pm = (m % 12) + 1; py = y + (1 if m == 12 else 0)
            f[0] = f"המדד הבא ({MONTHS[pm]} {py})"
            f[1] = f"יפורסם ב-15.{nm}.{ny}"
    t["source"] = {"name": f'הלמ"ס - נתוני מדד רשמיים (API), {mon}', "url": CBS_API_SRC}
    t["check"] = [f"{st['value']:g}", f"{st['yoy']:g}%"]
    t["effective"] = today(); t["checked"] = today()
    ny2, nm2 = next15(y, m, skip=2); t["next_review"] = f"{ny2}-{nm2:02d}-15"
    t["h1"] = t.get("h1", "")
    a["expect"] = {"period": period, "level": f"{st['value']:g}", "mom": f"{st['mom']:g}", "yoy": f"{st['yoy']:g}"}
    changes.insert(0, {"date": today(), "topic": t["slug"],
        "text": (f"מדד {mon}: {d} של {pct}%, רמה {st['value']:g}. קצב האינפלציה השנתי: {st['yoy']:g}%." if st["mom"] != 0
                else f"מדד {mon}: ללא שינוי, רמה {st['value']:g}. קצב האינפלציה השנתי: {st['yoy']:g}%.")})
    return True

def upd_boi(t, st, changes):
    a = t.setdefault("adapter", {"type": "boi_interest"})
    exp = a.get("expect", {})
    cur = f"{st['rate']:g}"
    changed = exp.get("rate") != cur
    decided = exp.get("published") != st["published"]
    if not changed and not decided:
        if exp.get("next") != st["next"]:
            pass  # next-date revision alone: update quietly below
        t["checked"] = today()
        t["next_review"] = st["next"]
        a["expect"] = {"rate": cur, "next": st["next"], "published": st["published"]}
        return changed
    # decision happened: rewrite
    dd = datetime.date.fromisoformat(st["published"])
    dds = f"{dd.day}.{dd.month}.{dd.year}"
    nd = datetime.date.fromisoformat(st["next"]); nds = f"{nd.day}.{nd.month}.{nd.year}"
    old = exp.get("rate")
    outcome = "ללא שינוי" if not changed else ("עלייה" if float(cur) > float(old) else "הורדה")
    if changed:
        outcome_txt = f"{outcome} ל-{cur}%"
    else:
        outcome_txt = "ללא שינוי"
    t["title"] = f"ריבית בנק ישראל היום: {cur}% | ההחלטה הבאה {nds}"
    rows = t["table"]["rows"]
    rows[0] = ["ריבית בנק ישראל נוכחית", f"{cur}%"]
    prev = rows[1][1] if len(rows) > 1 else ""
    rows[1] = ["ההחלטה האחרונה", f"{dds}: {outcome_txt}"]
    if len(rows) > 2 and prev:
        rows[2] = ["ההחלטה הקודמת", prev]
        del rows[3:]
    t["table"]["rows"] = rows[:3]
    prime = st["rate"] + 1.5
    for f in t.get("facts", []):
        if f[0].startswith("ריבית הפריים"):
            f[1] = f"{prime:g}% ({cur}% + 1.5%)"
    verb = "העלתה אותה ל-" if changed and outcome == "עלייה" else "הורידה אותה ל-"
    decision_phrase = f"{verb}{cur}%" if changed else "הותירה אותה ללא שינוי"
    t["intro"] = f"לפי בנק ישראל, הריבית עומדת על {cur}%. בהחלטה מ-{dds} הוועדה המוניטרית {decision_phrase}. ההחלטה הבאה צפויה ב-{nds}."
    t["answer"] = {"label": "ריבית בנק ישראל", "value": f"{cur}%",
                   "sub": f"{outcome_txt} בהחלטה מ-{dds} · ההחלטה הבאה {nds}"}
    t["source"] = {"name": f"בנק ישראל - ריבית בנק ישראל (API רשמי), החלטה מ-{dds}", "url": BOI}
    t["checked"] = today(); t["next_review"] = st["next"]
    t["check"] = [f"{cur}%"]
    a["expect"] = {"rate": cur, "next": st["next"], "published": st["published"]}
    txt = (f"בנק ישראל {'הותיר את הריבית על' if not changed else ('העלה את הריבית ל-' if outcome=='עלייה' else 'הוריד את הריבית ל-')}{cur}%"
           + (f" (מ-{old}%)" if changed and old else "") + f". ההחלטה הבאה ב-{nds}.")
    changes.insert(0, {"date": today(), "topic": t["slug"], "text": txt})
    return True

def main():
    apply = "--apply" in sys.argv
    D = json.loads(P.read_text(encoding="utf-8"))
    changes = D.setdefault("changes", [])
    failures, updated = [], []
    for t in D["topics"]:
        at = t.get("adapter", {}).get("type")
        if not at:
            continue
        try:
            st = fetch_cpi() if at == "cbs_cpi" else fetch_boi()
            fn = upd_cpi if at == "cbs_cpi" else upd_boi
            if fn(t, st, changes):
                updated.append(t["slug"])
        except Exception as ex:
            failures.append(f"{t['slug']}: {ex}")
    if failures:
        print("VALIDATION/FETCH FAILURES:")
        [print(" -", f) for f in failures]
        sys.exit(1)
    if updated:
        print("updated:", ", ".join(updated))
        if apply:
            P.write_text(json.dumps(D, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print("data.json written")
    else:
        print("all adapter topics already current; check dates refreshed" + (" (written)" if apply else ""))
        if apply:
            P.write_text(json.dumps(D, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if not apply:
        print("DRY RUN - nothing written")
if __name__ == "__main__":
    main()
