#!/usr/bin/env python3
"""Static Hebrew RTL site generator. data/data.json + CALCS below -> public/."""
import json, html, pathlib, os
root = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((root/"data/data.json").read_text(encoding="utf-8"))
pub = root/"public"; pub.mkdir(exist_ok=True)
S = D["site"]; e = html.escape
SITE_URL = os.environ.get("SITE_URL","https://example.com")
NOINDEX = os.environ.get("INDEX")!="1"   # staging = noindex. Production: INDEX=1 SITE_URL=https://domain
ADS = ""  # AdSense snippet after approval
def fmt(d):
    y,m,dd = d.split("-"); return f"{int(dd)}.{int(m)}.{y}"
ICON = {"pct":'<line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
"up":'<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
"drop":'<path d="M12 2.7l5.7 5.7a8 8 0 1 1-11.4 0z"/>',"bolt":'<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
"shield":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',"coin":'<circle cx="12" cy="12" r="9"/><path d="M14.8 9.2c-.5-.8-1.5-1.2-2.8-1.2-1.7 0-2.8.8-2.8 2s1 1.7 2.8 2 2.8.8 2.8 2-1.1 2-2.8 2c-1.3 0-2.4-.5-2.9-1.4M12 6v2m0 8v2"/>',
"bank":'<path d="M3 10l9-6 9 6M5 10v8m4-8v8m6-8v8m4-8v8M3 21h18"/>',"calc":'<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 11h2m4 0h2M8 15h2m4 0h2M8 19h2m4 0h2"/>',
"home":'<path d="M3 11l9-8 9 8v10H3z"/><path d="M9 21v-6h6v6"/>',"user":'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',"save":'<path d="M4 7h16v13H4z"/><path d="M8 7V4h8v3M12 11v5"/>',"search":'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>'}
def ic(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[n]}</svg>'
TIC = {"ribit-bank-israel":"bank","madad-hamechirim":"up","mechir-benzin":"drop","tarif-chashmal":"bolt","madregot-mas-hakhnasa":"pct","maam":"pct","sachar-minimum":"coin","bituach-leumi-shcirim":"shield","bituach-leumi-atzmaim":"shield"}
GIC = {"נתונים חודשיים":"up","מס":"pct","שכר וביטוח לאומי":"coin","קצבאות וגמלאות":"user","חיסכון פנסיוני":"save"}
def tic(t): return TIC.get(t["slug"], GIC.get(t["group"],"coin"))
cpi = {"דצמבר 2025":103.6,"ינואר 2026":103.3,"פברואר 2026":103.5,"מרץ 2026":103.9,"אפריל 2026":105.1,"מאי 2026":104.8,"יוני 2026":104.8,"יולי 2026":105.1,"אוגוסט 2026":105.8,"ספטמבר 2026":105.3}
RATES = {"taxM":[[7010,.10],[10060,.14],[19000,.20],[25100,.31],[46690,.35],[1e12,.47]],"taxY":[[84120,.10],[120720,.14],[228000,.20],[301200,.31],[560280,.35],[1e12,.47]],
 "point":242,"bl":{"low":7703,"max":51910,"empBLlow":.0104,"empBLhigh":.07,"empHlow":.0323,"empHhigh":.0517,"selfBLlow":.0447,"selfBLhigh":.1283,"selfHlow":.0323,"selfHhigh":.0517},
 "vat":18,"cpi":cpi,"boi":3.25,"fuel":7.77,"osekCeil":122833,"sevExempt":13750}
(pub/"js").mkdir(exist_ok=True)
(pub/"js/rates.js").write_text("window.RATES="+json.dumps(RATES)+";")
MONTHS=list(cpi)
def opts(lst,sel=None): return "".join(f'<option value="{e(str(v))}"{" selected" if str(v)==str(sel) else ""}>{e(l)}</option>' for v,l in lst)
def num(i,l,v,step="any",w=False,mn=None): return f'<label{" class=w" if w else ""}>{e(l)}<input type="number" inputmode="decimal" name="{i}" value="{v}" step="{step}"{f" min={mn}" if mn is not None else ""}></label>'
def sel(i,l,o,s=None,w=False): return f'<label{" class=w" if w else ""}>{e(l)}<select name="{i}">{opts(o,s)}</select></label>'
def dat(i,l,v): return f'<label>{e(l)}<input type="date" name="{i}" value="{v}"></label>'
mo=[(m,m) for m in MONTHS]
PTS=[("2.25","תושב: 2.25 נקודות"),("2.75","תושבת: 2.75 נקודות"),("3.25","נער: 3.25"),("3.75","נערה: 3.75")]
BTL="https://www.btl.gov.il/"; BK=D["topics"][0]["source"]["url"] if False else "https://www.gov.il/BlobFolder/generalpage/income-tax-monthly-deductions-booklet/he/generalInformation_income-tax-monthly-deductions-booklet_monthly-deductions-booklet-2026.pdf"
CK="2026-10-16"
CALCS=[
 dict(slug="machshevon-neto-2026",calc="net",icon="coin",title="מחשבון ברוטו נטו 2026",h1="מחשבון ברוטו נטו 2026 - כמה נשאר בכיס",short="ברוטו נטו",intro="הכניסו שכר ברוטו חודשי וקבלו הערכת נטו לפי מדרגות מס הכנסה, ביטוח לאומי וביטוח בריאות של 2026.",
  fields=num("gross","שכר ברוטו חודשי (₪)",12000,100)+sel("points","נקודות זיכוי",PTS,"2.25")+num("pension","הפרשת עובד לפנסיה (%)",0,"0.1",mn=0),
  assum=["מס הכנסה לפי מדרגות 2026 על שכר חודשי (עד 7,010 ₪ ב-10%, עד 10,060 ב-14%, עד 19,000 ב-20%, עד 25,100 ב-31%, עד 46,690 ב-35%, מעל ב-47%). נקודת זיכוי: 242 ₪ לחודש.","ביטוח לאומי: 1.04% עד 7,703 ₪ ו-7% עד 51,910 ₪. ביטוח בריאות: 3.23% ו-5.17% באותן מדרגות.","פנסיה, קרן השתלמות, שווי רכב והטבות אחרות אינם משפיעים על המס בחישוב הזה. הפרשת הפנסיה מנוכית מהנטו בלבד, ללא זיכוי מס.","הערכה לשכיר תושב ישראל עם משרה אחת. תלוש השכר בפועל עשוי להיות שונה."],
  src=[("מדרגות מס ונקודת זיכוי - לוח ניכויים 2026",BK),("שיעורי ביטוח לאומי ובריאות לשכירים",BTL+"INSURANCE/RATES/Pages/%D7%9C%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D%20%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D.aspx"),("נקודות זיכוי לתושבי ישראל - כל זכות","https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%9C%D7%AA%D7%95%D7%A9%D7%91_%D7%99%D7%A9%D7%A8%D7%90%D7%9C")],kw="ברוטו נטו שכר מחשבון משכורת תלוש מס"),
 dict(slug="machshevon-hatzmada-madad",calc="cpi",icon="up",title="מחשבון הצמדה למדד המחירים לצרכן",h1="מחשבון הצמדה למדד - הצמדת סכום בין שני חודשים",short="הצמדה למדד",intro="בחרו סכום וחודשי בסיס וסיום, וקבלו את הסכום אחרי הצמדה למדד המחירים לצרכן של הלמ\"ס.",
  fields=num("amount","סכום (₪)",5000,100,w=True)+sel("from","חודש מדד הבסיס",mo,"ינואר 2026")+sel("to","חודש מדד הסיום",mo,"ספטמבר 2026"),
  assum=["המדד לפי הודעות הלמ\"ס, בסיס ממוצע 2024=100: דצמבר 2025 103.6, ינואר 103.3, פברואר 103.5, מרץ 103.9, אפריל 105.1, מאי 104.8, יוני 104.8, יולי 105.1, אוגוסט 105.8, ספטמבר 105.3.","הסכום המוצמד = הסכום × מדד הסיום ÷ מדד הבסיס.","בחוזים שונים ההצמדה נעשית ל\"מדד הידוע\" או ל\"מדד בגין\" - בחרו את החודש לפי מה שכתוב בחוזה. החישוב כאן אינו מחליף את לשון החוזה.","נתוני יולי נלקחו מדיווחי התקשורת על הודעת הלמ\"ס. שאר החודשים מהודעות הלמ\"ס."],
  src=[("הודעת הלמ\"ס - מדד ספטמבר 2026","https://www.cbs.gov.il/he/mediarelease/Madad/DocLib/2026/326/10_26_326b.pdf"),("הודעת הלמ\"ס - מדד אוגוסט 2026","https://www.cbs.gov.il/he/mediarelease/Madad/DocLib/2026/293/10_26_293b.pdf")],kw="הצמדה למדד שכירות מדד המחירים לצרכן הצמדת סכום"),
 dict(slug="machshevon-maam",calc="vat",icon="pct",title="מחשבון מע\"מ 18% - הוספה והורדה",h1="מחשבון מע\"מ - הוספת מע\"מ והורדת מע\"מ",short="מע\"מ",intro="חישוב מהיר: מחיר כולל מע\"מ ממחיר לפני מע\"מ, או הפוך. שיעור המע\"מ בישראל הוא 18% מ-1.1.2025.",
  fields=num("amount","סכום (₪)",1000,"any",w=True)+sel("mode","מה לחשב",[("add","להוסיף מע\"מ"),("remove","להוריד מע\"מ (הסכום כולל מע\"מ)")],"add")+num("rate","שיעור מע\"מ (%)",18,"0.1"),
  assum=["שיעור המע\"מ הכללי: 18% מיום 1.1.2025 (היה 17%).","חישוב בסיסי. עסקאות בשיעור אפס או פטורות ממע\"מ אינן נכללות."],
  src=[("רשות המסים - הודעת הממשלה על העלאת המע\"מ ל-18%","https://www.gov.il/he/pages/dec1270-2024"),("רשות המסים - חוברת נטו מע\"מ","https://www.gov.il/BlobFolder/dynamiccollectorresultitem/netuachmaam-020626/he/vat_netuachmaam-020626.pdf")],kw="מע\"מ מחשבון הוספת מע\"מ הורדת מע\"מ 18%"),
 dict(slug="machshevon-pitzuyim",calc="sev",icon="shield",title="מחשבון פיצויי פיטורים",h1="מחשבון פיצויי פיטורים - חישוב לפי שנות ותק",short="פיצויי פיטורים",intro="הכניסו שכר חודשי אחרון ותאריכי עבודה וקבלו הערכת פיצויים בסיסית: שכר חודש אחד לכל שנת עבודה.",
  fields=num("salary","שכר חודשי אחרון (₪)",10000,100,w=True)+dat("start","תאריך תחילת עבודה","2021-01-01")+dat("end","תאריך סיום עבודה","2026-10-01"),
  assum=["סעיף 12(א) לחוק פיצויי פיטורים: שכר חודש אחד לכל שנת עבודה, וחלק משנה מזכה בפיצויים יחסיים.","החישוב מתאים לעובד במשכורת חודשית קבועה. שכר משתנה, שכר שבועי והפקדות לפי סעיף 14 אינם נכללים.","התשלום מוצג לפני מס. תקרת הפטור ממס הוצגה לידיעה בלבד."],
  src=[("חוק פיצויי פיטורים, סעיף 12 - הביטוח הלאומי (נוסח החוק)","https://www.btl.gov.il/Laws1/00_0040_000000.pdf"),("חישוב פיצויי פיטורים - כל זכות","https://www.kolzchut.org.il/he/%D7%97%D7%99%D7%A9%D7%95%D7%91_%D7%A4%D7%99%D7%A6%D7%95%D7%99%D7%99_%D7%A4%D7%99%D7%98%D7%95%D7%A8%D7%99%D7%9D"),("תקרת הפטור - לוח ניכויים 2026",BK)],kw="פיצויי פיטורים מחשבון פיצויים חישוב ותק"),
 dict(slug="machshevon-shaot-nosafot",calc="ot",icon="up",title="מחשבון שעות נוספות 125% 150%",h1="מחשבון שעות נוספות - 125% ו-150%",short="שעות נוספות",intro="חישוב גמול שעות נוספות: שעתיים ראשונות ב-125% ומהשעה השלישית ב-150%.",
  fields=num("rate","שכר שעתי רגיל (₪)",50,"0.1")+sel("thr","יום עבודה רגיל",[("8.6","5 ימים בשבוע: 8.6 שעות"),("8","6 ימים בשבוע: 8 שעות")],"8.6")+num("hours","שעות עבודה ביום",10,"0.25")+num("days","מספר ימים כאלה בחודש",20,1),
  assum=["לפי כל זכות ומשרד הממשלה: 125% מהשכר הרגיל לשעתיים הנוספות הראשונות ביום, ו-150% מהשעה השלישית.","יום עבודה רגיל: 8.6 שעות בשבוע עבודה של 5 ימים, 8 שעות בשישה ימים. חישוב שבועי, שעות במנוחה שבועית, וחגים אינם נכללים."],
  src=[("גמול עבור שעות נוספות - כל זכות","https://www.kolzchut.org.il/he/%D7%92%D7%9E%D7%95%D7%9C_%D7%A2%D7%91%D7%95%D7%A8_%D7%A9%D7%A2%D7%95%D7%AA_%D7%A0%D7%95%D7%A1%D7%A4%D7%95%D7%AA"),("שעות עבודה ושעות נוספות - כל זכות","https://www.kolzchut.org.il/he/%D7%AA%D7%A0%D7%90%D7%99_%D7%94%D7%A2%D7%A1%D7%A7%D7%AA_%D7%A2%D7%95%D7%91%D7%93_%D7%96%D7%A8")],kw="שעות נוספות 125 150 מחשבון גמול"),
 dict(slug="machshevon-mashkanta-shpitzer",calc="sh",icon="home",title="מחשבון משכנתא - לוח סילוקין שפיצר",h1="מחשבון משכנתא - החזר חודשי בשיטת שפיצר",short="משכנתא שפיצר",intro="החזר חודשי קבוע לפי לוח סילוקין שפיצר, סך הריבית ויתרת הקרן.",
  fields=num("amount","סכום ההלוואה (₪)",1000000,10000)+num("rate","ריבית שנתית (%)",4.5,"0.05")+num("years","מספר שנים",25,1),
  assum=["שיטת שפיצר: החזר חודשי קבוע, ריבית קבועה לכל התקופה, ללא הצמדה.","אין בחישוב ביטוחים, עמלות או שינוי ריבית."],src=[("נוסחת שפיצר - חישוב מתמטי; מידע על מסלולי משכנתא - בנק ישראל","https://www.boi.org.il/information/bank-paymnts/financial-education/competition-in-mortgages/")],kw="משכנתא מחשבון שפיצר לוח סילוקין החזר חודשי"),
 dict(slug="machshevon-mashkanta-prime",calc="prime",icon="bank",title="מחשבון משכנתא בריבית פריים",h1="מחשבון משכנתא במסלול פריים",short="משכנתא פריים",intro="החזר חודשי במסלול פריים ובדיקת רגישות לעליית ריבית. הפריים ברירת המחדל מחושב מריבית בנק ישראל ועוד 1.5%.",
  fields=num("amount","סכום המסלול (₪)",500000,10000)+num("prime","ריבית פריים (%)",4.75,"0.05")+num("margin","הנחה (-) או תוספת (+) לפריים (%)",-0.5,"0.05")+num("years","מספר שנים",25,1),
  assum=["ריבית בנק ישראל כעת 3.25%. ברירת המחדל של הפריים, 4.75%, היא 3.25% + 1.5%, לפי הנוהג בבנקים. זו אינה הגדרה רשמית שאימתנו, ואפשר לשנות אותה.","המסלול אינו צמוד למדד. עליית ריבית מחושבת כאילו חלה מיד על אותה יתרה ותקופה.","אין בחישוב עמלות וביטוחים."],
  src=[("ריבית בנק ישראל - הודעת הוועדה המוניטרית 1.9.2026","https://www.boi.org.il/publications/pressreleases/01-09-26/"),("מסלולי משכנתא - בנק ישראל","https://www.boi.org.il/information/bank-paymnts/financial-education/competition-in-mortgages/")],kw="משכנתא פריים מחשבון ריבית פריים החזר"),
 dict(slug="machshevon-mashkanta-tzmuda-madad",calc="mcpi",icon="home",title="מחשבון משכנתא צמודה למדד",h1="מחשבון משכנתא בריבית קבועה צמודה למדד",short="משכנתא צמודה",intro="הדגמה של החזר חודשי במסלול קבוע צמוד, בהנחת אינפלציה שנתית קבועה.",
  fields=num("amount","סכום המסלול (₪)",500000,10000)+num("rate","ריבית שנתית (%)",3.2,"0.05")+num("years","מספר שנים",25,1)+num("infl","אינפלציה שנתית צפויה (%)",2,"0.1"),
  assum=["במסלול קבוע צמוד הריבית קבועה והקרן מוצמדת למדד, ולכן כל עלייה במדד מעלה את ההחזר החודשי (בנק ישראל).","ההדגמה מניחה אינפלציה קבועה. האינפלציה ב-12 החודשים עד ספטמבר 2026: 1.6%.","אין בחישוב עמלות וביטוחים."],
  src=[("מסלולי משכנתא - בנק ישראל","https://www.boi.org.il/information/bank-paymnts/financial-education/competition-in-mortgages/"),("הודעת הלמ\"ס - מדד ספטמבר 2026","https://www.cbs.gov.il/he/mediarelease/Madad/DocLib/2026/326/10_26_326b.pdf")],kw="משכנתא צמודה מדד קבועה צמודה מחשבון"),
 dict(slug="machshevon-osek-patur-neto",calc="op",icon="user",title="מחשבון נטו לעוסק פטור",h1="מחשבון הכנסה נטו לעוסק פטור",short="נטו לעוסק פטור",intro="הערכה גסה של הכנסה נטו חודשית אחרי מס הכנסה וביטוח לאומי ובריאות, לפי מחזור והוצאות.",
  fields=num("rev","מחזור חודשי (₪)",8000,100)+num("exp","הוצאות חודשיות (₪)",1000,100)+sel("points","נקודות זיכוי",PTS,"2.25"),
  assum=["תקרת המחזור לעוסק פטור ב-2026: 122,833 ₪ לשנה (חישוב מ-1.1.2026).","מס הכנסה לפי המדרגות השנתיות של 2026, ביטוח לאומי ובריאות לעצמאי: 4.47%+3.23% עד 7,703 ₪ ו-12.83%+5.17% עד 51,910 ₪ לחודש. הבסיס לדמי הביטוח מופחת ב-52% מדמי הביטוח הלאומי, כמתואר בעמוד הביטוח הלאומי.","אין בחישוב ניכוי חלק מדמי הביטוח הלאומי במס, פנסיה או הוצאות מיוחדות. מטרת המחשבון להערכה בלבד."],
  src=[("תקרת עוסק פטור 2026 - כל זכות","https://www.kolzchut.org.il/he/%D7%A2%D7%95%D7%A1%D7%A7_%D7%A4%D7%98%D7%95%D7%A8"),("רשות המסים - רפורמת בעל עסק זעיר","https://www.gov.il/he/departments/topics/income-tax-small-business-owner-24"),("שיעורי דמי ביטוח לעצמאי",BTL+"Insurance/National%20Insurance/type_list/Self_Employed/Pages/rates.aspx"),("מדרגות מס - לוח ניכויים 2026",BK)],kw="עוסק פטור נטו מחשבון הכנסה מס ביטוח לאומי עצמאי"),
 dict(slug="machshevon-alut-delek-nesia",calc="fuel",icon="drop",title="מחשבון עלות דלק לנסיעה",h1="מחשבון עלות דלק לנסיעה - כמה עולה הנסיעה",short="עלות דלק לנסיעה",intro="מרחק, צריכת דלק ומחיר בנזין, וקבלו את עלות הדלק. מחיר ברירת המחדל הוא המחיר המרבי הנוכחי של בנזין 95 בשירות עצמי.",
  fields=num("km","מרחק (ק\"מ)",100,1)+num("l100","צריכה (ליטר ל-100 ק\"מ)",7,"0.1")+num("price","מחיר לליטר (₪)",7.77,"0.01")+sel("trip","סוג נסיעה",[("1","כיוון אחד"),("2","הלוך וחזור")],"1"),
  assum=["מחיר ברירת המחדל: המחיר המרבי לליטר בנזין 95 בשירות עצמי, כולל מע\"מ, מ-5.10.2026 (משרד האנרגיה). תחנות רשאיות למכור בפחות.","עלות דלק בלבד, ללא בלאי, ביטוח וכבישי אגרה."],
  src=[("משרד האנרגיה - עדכון מחיר הבנזין 5.10.2026","https://www.gov.il/he/pages/fuel-october-5-2026")],kw="עלות דלק נסיעה מחשבון בנזין צריכה"),
 dict(slug="machshevon-ribit-deribit",calc="ci",icon="up",title="מחשבון ריבית דריבית",h1="מחשבון ריבית דריבית עם הפקדה חודשית",short="ריבית דריבית",intro="כמה יצבור סכום התחלתי והפקדה חודשית בריבית שנתית קבועה, עם ריבית דריבית חודשית.",
  fields=num("p","סכום התחלתי (₪)",50000,1000)+num("m","הפקדה חודשית (₪)",1000,100)+num("rate","תשואה שנתית (%)",4,"0.1")+num("years","מספר שנים",15,1),
  assum=["תשואה קבועה ללא מס, דמי ניהול ואינפלציה. תשואות עתידיות אינן מובטחות.","הפקדה בסוף כל חודש, ריבית דריבית חודשית."],src=[("חישוב מתמטי של ריבית דריבית (אין מקור חיצוני נדרש)","")],kw="ריבית דריבית מחשבון חיסכון הפקדה חודשית")]
def head(title,desc,path,mod=None,extra=""):
    ld=('<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"inLanguage":"he","dateModified":mod,"description":desc},ensure_ascii=False)+'</script>') if mod else ''
    rb='<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    return f'''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#4338ca">
<title>{e(title)} | {e(S["name"])}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{SITE_URL}{path}">{rb}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:locale" content="he_IL"><meta property="og:type" content="article"><meta property="og:url" content="{SITE_URL}{path}">
<link rel="preload" href="/fonts/heebo-400.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="/css/style.css"><script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t;else if(matchMedia("(prefers-color-scheme:dark)").matches)document.documentElement.dataset.theme="dark"}}catch(e){{}}</script>{ld}{ADS}</head>'''
def shell(title,desc,body,path,mod=None,hero=None,cur=""):
    nav="".join(f'<a href="{u}"{" class=on" if cur==u else ""}>{l}</a>' for u,l in [("/","ראשי"),("/machshevonim/","מחשבונים"),("/mah-hishtana/","מה השתנה"),("/about/","אודות")])
    out=head(title,desc,path,mod)+f'''<body><header class="top"><div class="wrap"><div class="bar"><a class="brand" href="/"><span class="logo">{ic("up")}</span>{e(S["name"])}</a><div class="sp"></div>
<div class="sbox"><input id="q" type="search" placeholder="חיפוש באתר..." aria-label="חיפוש באתר" autocomplete="off"><div id="sres" class="sres"></div></div><button id="tbtn" class="tbtn" aria-label="מצב כהה או בהיר">◐</button></div><nav class="menu">{nav}</nav></div></header>
{hero or ""}<main class="wrap">{body}</main><footer><div class="wrap"><p>המידע באתר הוא הערכה למטרות מידע בלבד ואינו ייעוץ מס, משפטי או פיננסי. במקרה של סתירה גוברות הוראות הדין והמקור הרשמי.</p><p><a href="/about/">אודות</a> · <a href="/privacy/">פרטיות</a> · <a href="/disclaimer/">הבהרה משפטית</a></p></div></footer><script src="/js/app.js" defer></script>{{extra}}</body></html>'''
    return out
def write(path,html_): p=pub/path.strip("/"); p.mkdir(parents=True,exist_ok=True); (p/"index.html").write_text(html_,encoding="utf-8")
def page(title,desc,body,path,mod=None,hero=None,cur="",extra=""): write(path,shell(title,desc,body,path,mod,hero,cur).replace("{extra}",extra))
def table(t):
    h="".join(f"<th>{e(x)}</th>" for x in t["head"]); r="".join("<tr>"+"".join(f"<td>{e(c)}</td>" for c in row)+"</tr>" for row in t["rows"])
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'
topics={t["slug"]:t for t in D["topics"]}
def card(u,i,t,s): return f'<a class="card" href="{u}"><span class="ico">{ic(i)}</span><div><b>{e(t)}</b><span>{e(s)}</span></div></a>'
srcnote=lambda t:(lambda s:f'<div class="src">מקור: <a href="{e(s["url"])}" rel="noopener">{e(s["name"])}</a>'+(f' · <a href="{e(s["also"])}" rel="noopener">מקור נוסף</a>' if s.get("also") else "")+f' · נבדק: {fmt(t["checked"])}</div>')(t["source"])
for t in D["topics"]:
    a=t["answer"]; ch=[c for c in D["changes"] if c["topic"]==t["slug"]]
    chh="".join(f'<li><time>{fmt(c["date"])}</time>{e(c["text"])}</li>' for c in ch)
    rel="".join(card(f'/{x["slug"]}/',tic(x),x["short"],x["answer"]["value"]+" · "+x["answer"]["label"]) for x in D["topics"] if x["group"]==t["group"] and x["slug"]!=t["slug"])
    facts="".join(f"<li><b>{e(k)}:</b> {e(v)}</li>" for k,v in t["facts"]); notes="".join(f"<li>{e(n)}</li>" for n in t["notes"])
    nr=f' · בדיקה הבאה: {fmt(t["next_review"])}' if t.get("next_review") else ""
    cl=""
    rc=[c for c in CALCS if c["slug"] in {"net":"","":""} ] if False else []
    body=f'''<p class="crumbs"><a href="/">ראשי</a> › {e(t["group"])}</p><h1>{e(t.get("h1",t["title"]))}</h1>
<div class="answer"><span>{e(a["label"])}</span><b>{e(a["value"])}</b><small>{e(a["sub"])}</small></div>
<p class="lead">{e(t.get("intro",t["summary"]))}</p><p class="meta"><span class="chip">בתוקף מ-{fmt(t["effective"])}</span><span class="chip">נבדק {fmt(t["checked"])}{nr}</span></p>
{table(t["table"])}{"<ul class='facts'>"+facts+"</ul>" if facts else ""}{"<h2>שינויים אחרונים</h2><ul class='feed'>"+chh+"</ul>" if chh else ""}
<h2>הערות</h2><ul class="notes">{notes}</ul>{srcnote(t)}{"<h2>עוד בנושא</h2><div class='grid'>"+rel+"</div>" if rel else ""}'''
    page(t["title"],t.get("intro",t["summary"]),body,f"/{t['slug']}/",t["checked"])
# calculators
for c in CALCS:
    ass="".join(f"<li>{e(x)}</li>" for x in c["assum"]); src="".join((f'<li><a href="{e(u)}" rel="noopener">{e(n)}</a></li>' if u else f"<li>{e(n)}</li>") for n,u in c["src"])
    oth="".join(card(f'/{x["slug"]}/',x["icon"],x["short"],"מחשבון") for x in CALCS if x["slug"]!=c["slug"])[:] 
    body=f'''<p class="crumbs"><a href="/">ראשי</a> › <a href="/machshevonim/">מחשבונים</a></p><h1>{e(c["h1"])}</h1><p class="lead">{e(c["intro"])}</p>
<form class="calc" data-calc="{c["calc"]}" onsubmit="return false">{c["fields"]}</form><section id="out" class="result" aria-live="polite"></section>
<h2>הנחות החישוב</h2><ul class="notes">{ass}</ul><div class="src"><b>הערכה בלבד, לא ייעוץ.</b> נבדק {fmt(CK)}. מקורות:<ul>{src}</ul></div><h2>מחשבונים נוספים</h2><div class="grid">{oth}</div>'''
    page(c["title"],c["intro"],body,f"/{c['slug']}/",CK,cur="/machshevonim/",extra='<script src="/js/rates.js"></script><script src="/js/calc.js"></script>')
hub="".join(card(f'/{c["slug"]}/',c["icon"],c["short"],c["intro"][:70]+"...") for c in CALCS)
page("מחשבונים פיננסיים לישראל 2026","מחשבון ברוטו נטו, פיצויים, שעות נוספות, מע\"מ, משכנתא והצמדה למדד - לפי נתוני 2026.",f'<h1>מחשבונים</h1><p class="lead">כל מחשבון עובד בדפדפן, מיידית, על הנתונים המאומתים של 2026.</p><div class="grid">{hub}</div>',"/machshevonim/",CK,cur="/machshevonim/")
# home
live=[t for t in D["topics"] if t.get("live")]
tiles="".join(f'<a class="tile" href="/{t["slug"]}/"><i>{ic(tic(t))}</i><span>{e(t["short"])}</span><b>{e(t["answer"]["value"])}</b><small>{e(t["answer"]["sub"])}</small></a>' for t in live)
recent="".join(f'<li><time>{fmt(c["date"])} · <a href="/{c["topic"]}/">{e(topics[c["topic"]]["short"])}</a></time>{e(c["text"])}</li>' for c in sorted(D["changes"],key=lambda c:c["date"],reverse=True)[:6])
pop="".join(card(f'/{c["slug"]}/',c["icon"],c["short"],"מחשבון") for c in CALCS[:4])
order=["מס","שכר וביטוח לאומי","קצבאות וגמלאות","חיסכון פנסיוני"]; groups=""
for g in order:
    groups+=f'<h3>{e(g)}</h3><div class="grid">'+"".join(card(f'/{t["slug"]}/',tic(t),t["short"],t["answer"]["value"]+" · "+t["answer"]["label"]) for t in D["topics"] if t["group"]==g)+"</div>"
hero=f'<div class="hero"><div class="wrap"><h1>המספרים של ישראל,<br>מעודכנים מהמקור</h1><p>ריבית, מדד, דלק, חשמל, מס, שכר וקצבאות. כל נתון עם מקור רשמי ותאריך בדיקה, ומחשבונים שעובדים על הנתונים האלה.</p></div></div>'
body=f'<div class="tiles" style="margin-top:0;position:relative">{tiles}</div><h2 style="margin-top:.4em">מחשבונים פופולריים</h2><div class="grid">{pop}</div><p><a href="/machshevonim/">כל המחשבונים ←</a></p><h2>מה השתנה לאחרונה</h2><ul class="feed">{recent}</ul><p><a href="/mah-hishtana/">כל השינויים ←</a></p><h2>כל הנושאים</h2>{groups}'
page(S["name"]+" - "+S["tagline"],S["tagline"],body,"/",CK,hero=hero,cur="/")
allc="".join(f'<li><time>{fmt(c["date"])} · <a href="/{c["topic"]}/">{e(topics[c["topic"]]["short"])}</a></time>{e(c["text"])}</li>' for c in sorted(D["changes"],key=lambda c:c["date"],reverse=True))
page("מה השתנה - יומן שינויים בשיעורים ובקצבאות","יומן שינויים בשיעורי מס, שכר וקצבאות בישראל",f'<h1>מה השתנה</h1><p class="lead">יומן השינויים שזיהינו במקורות הרשמיים, מהחדש לישן.</p><ul class="feed">{allc}</ul>',"/mah-hishtana/",cur="/mah-hishtana/")
page("אודות","על האתר ושיטת העבודה",'''<h1>אודות</h1><p>האתר עוקב אחרי נתונים כספיים רשמיים בישראל: ריבית, מדד, דלק, חשמל, מדרגות מס, שכר מינימום, ביטוח לאומי, קצבאות ומע"מ. כל נתון מצוטט למקור ממשלתי עם תאריך בדיקה.</p><h2>איך מתעדכנים</h2><p>בדיקה אוטומטית מתוזמנת משווה את המקורות הרשמיים לערכים באתר. כשמזוהה שינוי, הערך מתעדכן ונרשם ביומן "מה השתנה".</p><h2>שקיפות</h2><p>חלק מהתוכן נכתב ומתוחזק בעזרת כלי בינה מלאכותית, ונבדק מול המקור הרשמי. האתר אינו גוף ממשלתי. ייתכנו טעויות - מצאתם? נשמח לתיקון.</p><h2>מימון</h2><p>האתר עשוי להציג מודעות, ובעתיד קישורי שותפים. קישור שותפים ימוסמן בבירור כשיוצג.</p>''',"/about/",cur="/about/")
page("מדיניות פרטיות","מדיניות פרטיות",'''<h1>מדיניות פרטיות</h1><p>האתר אינו דורש הרשמה ואינו אוסף פרטים אישיים. החישובים במחשבונים מתבצעים בדפדפן שלכם ואינם נשלחים אלינו.</p><p>כשיופעלו מודעות, ספקי צד שלישי (כגון Google AdSense) עשויים להשתמש בקובצי עוגיות כדי להציג מודעות ולמדוד ביצועים. ניתן לנהל העדפות מודעות בהגדרות החשבון שלכם ב-Google ובדפדפן.</p><p>האתר שומר בדפדפן בחירה של מצב כהה או בהיר.</p><p class="meta">TODO לפני העלאה: פרטי קשר, וחלון הסכמה לעוגיות אם נדרש.</p>''',"/privacy/")
page("הבהרה משפטית","הבהרה משפטית",'''<h1>הבהרה משפטית</h1><p>המידע והמחשבונים באתר נועדו להערכה ולמידע כללי בלבד. אינם ייעוץ מס, פנסיוני, פיננסי או משפטי, ואינם מחליפים פנייה לרשות המוסמכת או לבעל מקצוע מורשה.</p><p>אנו משתדלים לשקף במדויק את המקורות הרשמיים, אך ייתכנו עיכובים או טעויות. במקרה של סתירה גוברות הוראות הדין והמקור הרשמי. השימוש במידע ובמחשבונים באחריות המשתמש.</p><p>קישורי שותפים, אם יופיעו, ימוסמנו ועשויים להניב לאתר עמלה.</p>''',"/disclaimer/")
# search index
sx=[{"u":f"/{t['slug']}/","t":t.get("h1",t["title"]),"d":t["answer"]["value"]+" · "+t["answer"]["label"],"k":t["short"]+" "+t["summary"]} for t in D["topics"]]+[{"u":f"/{c['slug']}/","t":c["h1"],"d":"מחשבון","k":c["kw"]+" "+c["short"]} for c in CALCS]
(pub/"search.json").write_text(json.dumps(sx,ensure_ascii=False))
urls=["/","/machshevonim/","/mah-hishtana/","/about/","/privacy/","/disclaimer/"]+[f"/{t['slug']}/" for t in D["topics"]]+[f"/{c['slug']}/" for c in CALCS]
(pub/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE_URL}{u}</loc></url>" for u in urls)+"</urlset>")
(pub/"robots.txt").write_text("User-agent: *\nDisallow: /\n" if NOINDEX else f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print("built",len(urls),"pages")
