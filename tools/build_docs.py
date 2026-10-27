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

# ---- Hosted-site-only additions (never added to the skill's own viewers) ----
# potentiate.bio Google Tag Manager container (same GA4 property as the main site).
GTM_ID = "GTM-5L6TGJMX"
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
BRAND_BAR = """<style>
.pb-bar{background:#244E54;color:#FBFAF6;font:500 13px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
.pb-bar .pb-in{max-width:1180px;margin:0 auto;padding:9px 16px;display:flex;gap:14px;align-items:center;justify-content:space-between}
.pb-bar a{color:inherit;text-decoration:none}
.pb-bar .pb-mark{font-weight:800;letter-spacing:-.02em;font-size:15px}
.pb-bar .pb-mark span{color:#F27A7D}
.pb-bar nav{display:flex;gap:14px;align-items:center}
.pb-bar nav a{opacity:.85}.pb-bar nav a:hover{opacity:1}
.pb-bar .pb-sub{background:#F27A7D;color:#244E54;padding:5px 10px;border-radius:999px;font-weight:700;opacity:1}
@media (max-width:480px){.pb-bar .pb-hide{display:none}}
</style>
<div class="pb-bar" data-track-area="nav"><div class="pb-in">
  <a class="pb-mark" href="https://potentiate.bio" data-track="nav_click" data-track-name="logo">p<span>.</span>b</a>
  <nav>
    <a class="pb-hide" href="index.html" data-track="nav_click" data-track-name="tools_home">Thoughtful outreach</a>
    <a href="https://potentiate.bio" data-track="nav_click" data-track-name="potentiate_bio">potentiate.bio</a>
    <a class="pb-sub" href="%s" data-track="subscribe_click" data-track-name="subscribe">Subscribe</a>
  </nav>
</div></div>
""" % SUBSCRIBE
# Pushes named clicks into GTM's dataLayer using the main site's event names and parameters.
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
PRIVACY = ("Lists you load stay in this browser — nothing is uploaded. This site only counts visits with Google Analytics.")


def hosted(html):
    assert html.count("<head>") == 1 and html.count("<body>") == 1
    html = html.replace("<head>", "<head>\n" + GTM_HEAD, 1)
    return html.replace("<body>", "<body>\n" + GTM_BODY + BRAND_BAR + TRACK, 1)


inject = '<script src="data/demo-data.js"></script>\n<script>window.DEMO_AUTOLOAD = true;</script>\n<script>\n(function(){'
for page in ("target-map.html", "briefing.html"):
    html = read(os.path.join(SKILL, "assets", page)).replace("https://github.com/potentiate-bio/thoughtful-outreach", REPO_URL)
    assert html.count("<script>\n(function(){") == 1, page
    html = html.replace("<script>\n(function(){", inject, 1)
    html = html.replace("Everything stays in this browser — nothing is uploaded.", PRIVACY)
    with open(os.path.join(DOCS, page), "w", encoding="utf-8") as f:
        f.write(hosted(html))

index = read(os.path.join(ROOT, "tools", "landing.html")).replace("https://github.com/potentiate-bio/thoughtful-outreach", REPO_URL)
for label, name in (("Try the target map", "try_target_map"), ("See a research briefing", "see_briefing"), ("Get the skill", "get_skill")):
    index = index.replace(">" + label + "</a>", ' data-track="cta_click" data-track-name="%s">%s</a>' % (name, label), 1)
with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
    f.write(hosted(index))
open(os.path.join(DOCS, ".nojekyll"), "w").close()
print("docs/ built:", sorted(os.listdir(DOCS)))
