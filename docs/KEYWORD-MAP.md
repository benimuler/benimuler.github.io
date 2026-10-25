# Keyword map (research date 2026-10-16)

Method: Hebrew web search for ~60 candidate queries; for each, looked at the top 5-10 results: who ranks (official bodies vs commercial/advisory sites vs small sites), whether results contain the exact 2026 number, how many are dated 2026. NO search-volume data was available (no keyword tool) - volume is unknown. Competition is a proxy only. Real validation = Search Console after launch.

## Rule of thumb from the data
- Queries about BTL/BoI/CBS/gov numbers (min wage, BTL rates, brackets, pensions, child allowance): top 5 is nearly all btl.gov.il / gov.il / wikipedia. Do NOT chase these head terms.
- Queries about pension/provident/keren-hishtalmut ceilings and tax exemptions: top results are commercial advisors (analyst.co.il, as-invest, mvs, pensuni, meidahon, moreinvest) and small accountants - beatable by a clean, dated, cited page. These also have high commercial value (pension/insurance advertisers), so they are the priority.
- Freshness queries (fuel, CPI, BoI) are news/small-site dominated and time-sensitive: win only by being updated right after each release.
- New-domain caveat: authority is zero. Expect months, not days. Pages with the exact number + 2026 + source citation + visible update date are the entry ticket.

## Priority queries (pick 15)
| # | Query | Landing page | Who ranks now (top) | Competition |
|---|---|---|---|---|
| 1 | תקרת קרן השתלמות לעצמאים 2026 | /taksrot-keren-hishtalmut-2026/ | analyst, pensuni, meidahon, madadim-c, clalbit (0 official in top 5) | Low-medium |
| 2 | משכורת קובעת לקרן השתלמות 2026 | same | as-invest, clalbit, analyst, themarker | Medium |
| 3 | תקרת הפקדה מוטבת קרן השתלמות 2026 | same | bizportal, analyst, themarker, homefinance | Medium |
| 4 | תקרת הפרשות מעסיק לקופת גמל 2026 | /taksrot-hafrashot-kupat-gemel-2026/ | as-invest, shekelgroup, mvs, neto.work (0 official) | Low |
| 5 | תקרת פיצויים להפקדה בקופת גמל | same | mvs, moreinvest, prisha, as-invest (0 official) | Low |
| 6 | תקרת הכנסה לעמית עצמאי פנסיה 2026 | same | clalbit, analyst, pensuni, bizportal | Low-medium |
| 7 | קצבה מזכה פטור 2026 תקרה | /ptor-kitzba-mezakkah-maanak-prisha-2026/ | gov.il then yuvalim-ins, shekelgroup, prisha | Medium |
| 8 | פטור ממס מענק הון פרישה 2026 | same | gov.il, meidahon, maximumcenter, mia-tax | Medium |
| 9 | תקרת פטור ממס על פרס מהגרלה 2026 | /ptor-mas-hagrala-prasim-milga-2026/ | ice, y-tax, pais, calcfinance (0 official in top 5) | Low |
| 10 | פטור ממס למלגה אצל חוקר | same | segel, protocol, university pages; no exact answer in results | Low (low volume) |
| 11 | פטור ממס על שכר דירה תקרה 2026 | /ptor-mas-schar-dira-2026/ | gov.il, tax firms, globes, bizportal | Medium-high |
| 12 | זיכוי מס תרומות סעיף 46 תקרה 2026 | /zikui-mas-tmuma-taksrot-2026/ | gov.il, deloitte, pwc, bizportal | Medium |
| 13 | מחיר בנזין 95 שירות עצמי (אחרי כל עדכון חודשי) | /mechir-benzin/ | gov.il, israelhayom, doralon, mechushav, autocom | Medium; needs 1st-of-month update |
| 14 | כמה עולה קוט"ש חשמל לבית 2026 | /tarif-chashmal/ | iec.co.il, kolhabait, themarker, shtipser, calculatzia | Medium |
| 15 | כמה עלה המדד בספטמבר 2026 / מדד המחירים לצרכן | /madad-hamechirim/ | cbs, tv10, themarker, funder | Medium-high, short-lived |

## Avoid (head terms owned by official sites)
שכר מינימום 2026, מדרגות מס הכנסה 2026, קצבת ילדים/זקנה/נכות 2026, דמי אבטלה, דמי ביטוח לאומי עצמאים 2026, ריבית בנק ישראל היום. Keep these pages (credibility, internal links, the "what changed" feed) but do not expect traffic from them.

## Next content to fill the gap
Pages for the weak-competition cluster need explanatory text, not just numbers (competitors explain). Only add explanations verified from official sources (do not write rules from memory). Candidates: keren hishtalmut deposit rates and tax benefit conditions, pension deposit percentages. Not yet verified, so not on the site.

## Positioning
Each page: exact query phrase in title + H1, the answer (number + year + unit) in the first sentence, visible "checked on" date, source link, Article JSON-LD with dateModified. Done in build.py for all pages.
