#!/usr/bin/env python3
"""Build the GitHub Pages demo site into docs/ (served at tools.potentiate.bio/thoughtful-outreach/).

Copies the two viewers from the skill, injects the fictional demo data so the pages open
pre-loaded, and writes the tool's landing page. Hosted pages also get the potentiate.bio
look (tools/brand/), a site header with breadcrumbs and a back link, and the site's Google
Tag Manager container. None of that is added to the viewers in skills/, which stay
self-contained and tracking-free for people running the skill on their own lists.

Run after changing the viewers or regenerating demo data:  python3 tools/build_docs.py
"""
import json, os, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(ROOT, "skills", "target-list-research")
DEMO = os.path.join(ROOT, "examples", "demo-event")
BRAND = os.path.join(ROOT, "tools", "brand")
DOCS = os.path.join(ROOT, "docs")
REPO_URL = os.environ.get("REPO_URL", "https://github.com/potentiate-bio/thoughtful-outreach")
TOOLS_HOME = "https://tools.potentiate.bio/"
TOOL_NAME = "Thoughtful outreach"

os.makedirs(os.path.join(DOCS, "data"), exist_ok=True)
os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)


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
for fn in ("pb-mark.png", "pb-icon-32.png", "pb-icon-180.png", "pb-icon-512.png"):
    shutil.copy(os.path.join(BRAND, fn), os.path.join(DOCS, "assets", fn))

# ---- Hosted-site-only additions ----
GTM_ID = "GTM-5L6TGJMX"   # potentiate.bio container — same GA4 property as the main site
GTM_HEAD = ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
            "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            "})(window,document,'script','dataLayer','%s');</script>\n<!-- End Google Tag Manager -->\n" % GTM_ID)
GTM_BODY = ('<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s" '
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
            '<!-- End Google Tag Manager (noscript) -->\n' % GTM_ID)
SUBSCRIBE = ("https://potentiate.beehiiv.com/subscribe?utm_source=tools.potentiate.bio"
             "&utm_medium=website&utm_campaign=subscribe_button")
HEAD_EXTRA = ('<link rel="icon" type="image/png" sizes="32x32" href="assets/pb-icon-32.png">\n'
              '<link rel="apple-touch-icon" href="assets/pb-icon-180.png">\n'
              '<meta property="og:image" content="https://tools.potentiate.bio/thoughtful-outreach/assets/pb-icon-512.png">\n'
              '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Unbounded:wght@600;700;800&display=swap" rel="stylesheet">\n'
              "<style>\n" + read(os.path.join(BRAND, "hosted.css")) + "</style>\n")
BACK_ICON = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3 5 8l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
TRACK = """<script>
(function(){
  window.dataLayer = window.dataLayer || [];
  var page = (location.pathname.split("/").pop() || "index.html").replace(".html","");
  document.addEventListener("click", function(e){
    var el = e.target.closest && e.target.closest("[data-track]"); if(!el) return;
    var area = el.closest("[data-track-area]");
    window.dataLayer.push({event: el.getAttribute("data-track"),
      click_name: el.getAttribute("data-track-name") || "",
      click_location: area ? area.getAttribute("data-track-area") : page,
      link_text: (el.textContent || "").trim().slice(0,80), link_url: el.href || ""});
  }, true);
})();
</script>
"""
PRIVACY = "Lists you load stay in this browser. Nothing is uploaded. This site only counts visits with Google Analytics."


def header(current, back=None):
    """Site header: logo → potentiate.bio, breadcrumb Tools › tool › page, All tools + Subscribe.
    `back` adds a prominent back link under the header on pages below the tool's landing page."""
    crumbs = ['<a href="%s" data-track="nav_click" data-track-name="tools_home">Tools</a>' % TOOLS_HOME]
    if current is None:
        crumbs.append('<span class="sep" aria-hidden="true">›</span><span aria-current="page">%s</span>' % TOOL_NAME)
    else:
        crumbs.append('<span class="sep pb-mid" aria-hidden="true">›</span><a class="pb-mid" href="index.html" '
                      'data-track="nav_click" data-track-name="tool_home">%s</a>' % TOOL_NAME)
        crumbs.append('<span class="sep" aria-hidden="true">›</span><span aria-current="page">%s</span>' % current)
    html = ('<header class="pb-head" data-track-area="nav"><div class="pb-in">\n'
            '  <a class="pb-logo" href="https://potentiate.bio" aria-label="potentiate.bio home" data-track="nav_click" '
            'data-track-name="logo"><img src="assets/pb-mark.png" alt="p.b" width="54" height="30"></a>\n'
            '  <nav class="pb-crumbs" aria-label="Breadcrumb">%s</nav>\n'
            '  <div class="pb-right"><a class="pb-link" href="%s" data-track="nav_click" data-track-name="all_tools">All tools</a>'
            '<a class="pb-sub" href="%s" data-track="subscribe_click" data-track-name="subscribe">Subscribe</a></div>\n'
            '</div></header>\n') % ("".join(crumbs), TOOLS_HOME, SUBSCRIBE)
    if back:
        html += ('<div class="pb-back" data-track-area="page"><a href="index.html" data-track="nav_click" '
                 'data-track-name="back_to_tool">%s%s</a></div>\n') % (BACK_ICON, back)
    return html


def hosted(html, current=None, back=None):
    assert html.count("</head>") == 1 and html.count("<body>") == 1
    html = html.replace("<html lang=\"en\">", "<html lang=\"en\" data-theme=\"light\">", 1)
    html = html.replace("<head>", "<head>\n" + GTM_HEAD, 1)
    html = html.replace("</head>", HEAD_EXTRA + "</head>", 1)
    return html.replace("<body>", "<body>\n" + GTM_BODY + header(current, back) + TRACK, 1)


inject = '<script src="data/demo-data.js"></script>\n<script>window.DEMO_AUTOLOAD = true;</script>\n<script>\n(function(){'
for page, label in (("target-map.html", "Target map"), ("briefing.html", "Research briefing")):
    html = read(os.path.join(SKILL, "assets", page)).replace("https://github.com/potentiate-bio/thoughtful-outreach", REPO_URL)
    assert html.count("<script>\n(function(){") == 1, page
    html = html.replace("<script>\n(function(){", inject, 1)
    html = html.replace("Everything stays in this browser — nothing is uploaded.", PRIVACY)
    html = html.replace("<title>Target Map</title>", "<title>Target map · Thoughtful outreach · potentiate.bio</title>")
    html = html.replace("<title>Research Briefing</title>", "<title>Research briefing · Thoughtful outreach · potentiate.bio</title>")
    with open(os.path.join(DOCS, page), "w", encoding="utf-8") as f:
        f.write(hosted(html, current=label, back="Back to Thoughtful outreach"))

index = read(os.path.join(ROOT, "tools", "landing.html")).replace("https://github.com/potentiate-bio/thoughtful-outreach", REPO_URL)
index = index.replace('<html lang="en" data-theme="light">', '<html lang="en">', 1)
for label, name in (("Try the target map", "try_target_map"), ("See a research briefing", "see_briefing"), ("Get the skill", "get_skill"), ("Read why I built it", "read_story")):
    index = index.replace(">" + label + "</a>", ' data-track="cta_click" data-track-name="%s">%s</a>' % (name, label), 1)
with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
    f.write(hosted(index))
open(os.path.join(DOCS, ".nojekyll"), "w").close()
print("docs/ built:", sorted(os.listdir(DOCS)))
