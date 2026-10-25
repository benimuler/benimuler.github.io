#!/usr/bin/env python3
"""Generate static Hebrew RTL site from data/data.json into public/."""
import json, html, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((root/"data/data.json").read_text(encoding="utf-8"))
pub = root/"public"; pub.mkdir(exist_ok=True)
S = D["site"]; e = html.escape
SITE_URL = "https://example.co.il"  # TODO: set after domain chosen
ADS = ""  # TODO: AdSense script goes here after approval (ca-pub id)
def fmt(d):
    y,m,dd = d.split("-"); return f"{int(dd)}.{int(m)}.{y}"
def page(title, desc, body, path):
    nav = '<a href="/">ראשי</a><a href="/mah-hishtana/">מה השתנה</a><a href="/about/">אודות</a>'
    out = f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | {e(S["name"])}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE_URL}{path}"><link rel="stylesheet" href="/css/style.css">{ADS}</head><body>
<header><a class="brand" href="/">{e(S["name"])}</a><nav>{nav}</nav></header><main>{body}</main>
<footer><p>המידע באתר הוא הערכה למטרות מידע בלבד ואינו ייעוץ מס, משפטי או פיננסי. במקרה של סתירה גוברות הוראות הדין והמקור הרשמי.</p>
<p><a href="/about/">אודות</a> · <a href="/privacy/">פרטיות</a> · <a href="/disclaimer/">הבהרה משפטית</a></p></footer></body></html>'''
    p = pub/path.strip("/"); p.mkdir(parents=True, exist_ok=True); (p/"index.html").write_text(out, encoding="utf-8")
def table(t):
    h = "".join(f"<th>{e(x)}</th>" for x in t["head"])
    r = "".join("<tr>"+"".join(f"<td>{e(c)}</td>" for c in row)+"</tr>" for row in t["rows"])
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'
topics = {t["slug"]:t for t in D["topics"]}
for t in D["topics"]:
    facts = "".join(f"<li><b>{e(k)}:</b> {e(v)}</li>" for k,v in t["facts"])
    notes = "".join(f"<li>{e(n)}</li>" for n in t["notes"])
    ch = [c for c in D["changes"] if c["topic"]==t["slug"]]
    chh = "".join(f'<li><time>{fmt(c["date"])}</time> {e(c["text"])}</li>' for c in ch)
    s = t["source"]; also = f' · <a href="{e(s["also"])}" rel="noopener">מקור נוסף</a>' if s.get("also") else ""
    body = f'''<h1>{e(t["title"])}</h1><p class="lead">{e(t["summary"])}</p>
<p class="meta">בתוקף מ-{fmt(t["effective"])} · נבדק לאחרונה: {fmt(t["checked"])}</p>
{table(t["table"])}{"<ul class='facts'>"+facts+"</ul>" if facts else ""}
{"<h2>שינויים אחרונים</h2><ul>"+chh+"</ul>" if chh else ""}
<h2>הערות</h2><ul>{notes}</ul>
<p class="src">מקור: <a href="{e(s["url"])}" rel="noopener">{e(s["name"])}</a>{also}</p>'''
    page(t["title"], t["summary"], body, f"/{t['slug']}/")
order=["מס","שכר וביטוח לאומי","קצבאות וגמלאות","חיסכון פנסיוני"]
cards = ""
for g in order:
    items = "".join(f'<li><a href="/{t["slug"]}/"><b>{e(t["short"])}</b><span>{e(t["summary"])}</span></a></li>' for t in D["topics"] if t["group"]==g)
    cards += f'<h3>{e(g)}</h3><ul class="cards">{items}</ul>'
recent = "".join(f'<li><time>{fmt(c["date"])}</time> <a href="/{c["topic"]}/">{e(topics[c["topic"]]["short"])}</a>: {e(c["text"])}</li>' for c in sorted(D["changes"], key=lambda c:c["date"], reverse=True)[:5])
page(S["name"], S["tagline"], f'<h1>{e(S["tagline"])}</h1><p class="lead">כל נתון מצוטט למקור רשמי עם תאריך בדיקה. נבדק לאחרונה: {fmt(S["verified"])}.</p><h2>מה השתנה לאחרונה</h2><ul>{recent}</ul><p><a href="/mah-hishtana/">כל השינויים</a></p><h2>נושאים</h2>{cards}', "/")
allc = "".join(f'<li><time>{fmt(c["date"])}</time> <a href="/{c["topic"]}/">{e(topics[c["topic"]]["short"])}</a>: {e(c["text"])}</li>' for c in sorted(D["changes"], key=lambda c:c["date"], reverse=True))
page("מה השתנה", "יומן שינויים בשיעורי מס, שכר וקצבאות בישראל", f'<h1>מה השתנה</h1><p class="lead">יומן השינויים שזיהינו במקורות הרשמיים, מהחדש לישן.</p><ul>{allc}</ul>', "/mah-hishtana/")
page("אודות", "על האתר ושיטת העבודה", '''<h1>אודות</h1><p>האתר עוקב אחרי נתונים כספיים רשמיים בישראל: מדרגות מס, שכר מינימום, ביטוח לאומי, קצבאות ומע"מ. כל נתון מצוטט למקור ממשלתי עם תאריך בדיקה.</p>
<h2>איך מתעדכנים</h2><p>בדיקה אוטומטית מתוזמנת משווה את המקורות הרשמיים לערכים באתר. כשמזוהה שינוי, הערך מתעדכן ונרשם ביומן "מה השתנה".</p>
<h2>שקיפות</h2><p>חלק מהתוכן נכתב ומתוחזק בעזרת כלי בינה מלאכותית, ונבדק מול המקור הרשמי. האתר אינו גוף ממשלתי. ייתכנו טעויות - מצאתם? נשמח לתיקון.</p>
<h2>מימון</h2><p>האתר עשוי להציג מודעות, ובעתיד קישורי שותפים. קישור שותפים ימוסמן בבירור כשיוצג.</p>''', "/about/")
page("מדיניות פרטיות", "מדיניות פרטיות", '''<h1>מדיניות פרטיות</h1><p>האתר אינו דורש הרשמה ואינו אוסף פרטים אישיים ישירות.</p>
<p>כשיופעלו מודעות, ספקי צד שלישי (כגון Google AdSense) עשויים להשתמש בקובצי עוגיות כדי להציג מודעות ולמדוד ביצועים. ניתן לנהל העדפות מודעות בהגדרות החשבון שלכם ב-Google ובדפדפן.</p>
<p>ייתכנו נתוני גלישה אנונימיים בשרת האירוח. לא נמכור מידע אישי.</p><p class="meta">TODO לפני העלאה: להוסיף פרטי קשר, וחלון הסכמה לעוגיות אם נדרש.</p>''', "/privacy/")
page("הבהרה משפטית", "הבהרה משפטית", '''<h1>הבהרה משפטית</h1><p>המידע באתר נועד להערכה ולמידע כללי בלבד. אינו ייעוץ מס, ייעוץ פיננסי, ייעוץ פנסיוני או ייעוץ משפטי, ואינו מחליף פנייה לרשות המוסמכת או לבעל מקצוע מורשה.</p>
<p>אנו משתדלים לשקף במדויק את המקורות הרשמיים, אך ייתכנו עיכובים או טעויות. במקרה של סתירה גוברות הוראות הדין והמקור הרשמי. השימוש במידע באחריות המשתמש.</p>
<p>קישורי שותפים, אם יופיעו, ימוסמנו ועשויים להניב לאתר עמלה.</p>''', "/disclaimer/")
urls = ["/","/mah-hishtana/","/about/","/privacy/","/disclaimer/"]+[f"/{t['slug']}/" for t in D["topics"]]
(pub/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE_URL}{u}</loc></url>" for u in urls)+"</urlset>")
(pub/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print("built", len(urls), "pages")
