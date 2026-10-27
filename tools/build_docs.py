#!/usr/bin/env python3
"""Build the GitHub Pages demo site into docs/.

Copies the two viewers from the skill, injects the fictional demo data so the pages
open pre-loaded, and writes a small landing page. Run after changing the viewers or
regenerating demo data:  python3 tools/build_docs.py

Set REPO_URL (env var) to the public repository URL before publishing.
"""
import json, os, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(ROOT, "skills", "target-list-research")
DEMO = os.path.join(ROOT, "examples", "demo-event")
DOCS = os.path.join(ROOT, "docs")
REPO_URL = os.environ.get("REPO_URL", "https://github.com/potentiate-bio/thoughtful-outreach")

os.makedirs(os.path.join(DOCS, "data"), exist_ok=True)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


# Demo data as JS so the pages work from file:// as well as over https
js = "window.DEMO_SCORED_CSV = %s;\nwindow.DEMO_RESEARCH_CSV = %s;\n" % (
    json.dumps(read(os.path.join(DEMO, "scored.csv"))), json.dumps(read(os.path.join(DEMO, "research.csv"))))
with open(os.path.join(DOCS, "data", "demo-data.js"), "w", encoding="utf-8") as f:
    f.write(js)
for fn in ("scored.csv", "research.csv", "attendees.csv", "overrides-example.csv"):
    shutil.copy(os.path.join(DEMO, fn), os.path.join(DOCS, "data", fn))

inject = '<script src="data/demo-data.js"></script>\n<script>window.DEMO_AUTOLOAD = true;</script>\n<script>\n(function(){'
for page in ("target-map.html", "briefing.html"):
    html = read(os.path.join(SKILL, "assets", page)).replace("https://github.com/potentiate-bio/thoughtful-outreach", REPO_URL)
    assert html.count("<script>\n(function(){") == 1, page
    html = html.replace("<script>\n(function(){", inject, 1)
    with open(os.path.join(DOCS, page), "w", encoding="utf-8") as f:
        f.write(html)

index = read(os.path.join(ROOT, "tools", "landing.html")).replace("https://github.com/potentiate-bio/thoughtful-outreach", REPO_URL)
with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
    f.write(index)
open(os.path.join(DOCS, ".nojekyll"), "w").close()
print("docs/ built:", sorted(os.listdir(DOCS)))
