# מדד השיעורים - live Israeli rates tracker (v0)
Static Hebrew RTL site. `data/data.json` is the single source of truth; `scripts/build.py` renders `public/`.
Deploy target (later): Render static site, publish dir `public/`, build cmd `python3 scripts/build.py`.
Update loop: scheduled agent runs `scripts/check.py` (fetches each official source, confirms published key values still appear). Drift -> agent reads source, edits data.json (values, effective, checked, add changes entry), builds, commits to GitHub -> Render redeploys.
Not yet visually checked in a browser. Before launch: set SITE_URL + ADS in build.py, add contact to privacy page.
Sources not machine-readable: gov.il/btl pages are HTML/PDF only (no API), so detection is string-match on key values + manual read on drift. Annual events: Jan 1 (BTL thresholds, benefits), Apr 1 (min wage), Jan (tax booklet).

## Deploy (one action once access exists)
1. Create GitHub repo (benimuler/<name>), `git init && git add . && git commit && git push` (public/ is generated, committed too so Render can serve even without a build).
2. Render: New > Blueprint > pick repo (reads render.yaml), or New Static Site: build `python3 scripts/build.py`, publish `public`. Free tier.
3. Custom domain: Render Settings > Custom Domains, then DNS CNAME at registrar. Set SITE_URL in scripts/build.py, rebuild, push.
4. .github/workflows/check.yml runs check.py weekly and fails on drift; the scheduled agent handles the actual update.
