# Search Console + indexing launch checklist (run after deploy)

Before going live
- [ ] Staging is noindex: the site builds with noindex + robots Disallow unless INDEX=1. Render's temp *.onrender.com URL must stay noindex.
- [ ] Production build: SITE_URL=https://<domain> INDEX=1 python3 scripts/build.py (set both as Render env vars + build command). Confirm robots.txt shows Allow + Sitemap, canonical tags show the real domain, no noindex meta.
- [ ] Redirect: www -> apex (or reverse) and http -> https; one canonical host only. Disable indexing of the onrender.com host after the custom domain works.
- [ ] Check privacy/about/disclaimer pages complete (contact detail) - needed for AdSense and trust.

Day 0
- [ ] Add a Domain property in Google Search Console, verify via DNS TXT at the registrar.
- [ ] Submit https://<domain>/sitemap.xml. Check status "Success".
- [ ] URL Inspection > Request indexing for: home, change feed, and the 8 priority landing pages in KEYWORD-MAP.md.
- [ ] Bing Webmaster Tools: import from Search Console, submit sitemap (cheap extra traffic).
- [ ] Validate structured data on 2 pages (Rich Results Test), run PageSpeed Insights mobile on home + 1 data page (target all green; site is static, should pass).

Week 1-4
- [ ] Coverage report: no "Excluded by noindex", no soft 404s, no "Duplicate without user-selected canonical".
- [ ] Weekly: export Performance report (queries, pages, impressions, avg position). Impressions without clicks = title/H1 mismatch to fix. This is also the first real search-volume data: re-rank the keyword map from it.
- [ ] After every monthly data refresh (fuel on the 1st, CPI on the 15th, BoI decision dates): update data.json, rebuild, push, and re-request indexing for that page.

Ongoing
- [ ] Annual refresh each January (tax booklet, BTL thresholds) and April (min wage); update the page title year.
- [ ] Do not buy backlinks. Earn them: send the "what changed this month" page to finance bloggers/journalists; cite-able numbers with sources are the link magnet.
- [ ] AdSense only after the site has traffic and the content pages are substantial; ads.txt at site root once approved.
