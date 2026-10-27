#!/usr/bin/env python3
"""Generate the fictional demo dataset used by the live viewer and the README.

Everything produced here is invented: the vendor ("Northwind Bioanalysis", a regulated
bioanalysis CRO), the event ("Atlantic Regulated Bioanalysis Workshop"), every company and
every person. Domains use the reserved `.example` TLD so no generated email address can
belong to anyone. Any resemblance to real organisations or people is coincidental.

Run from the repo root:  python3 tools/make_demo_data.py
Writes to examples/demo-event/.
"""
import csv, os, random

random.seed(20271027)
OUTDIR = os.path.join(os.path.dirname(__file__), "..", "examples", "demo-event")
os.makedirs(OUTDIR, exist_ok=True)
EVENT = "Atlantic Regulated Bioanalysis Workshop 2027"

TIER_NAMES = {"A": "Direct fit", "B": "Plausible", "C": "Partner / referral", "X": "Out of scope"}

# Segment keys -> title pool
SPONSOR_SM = "Clinical-stage sponsor — small molecule"
SPONSOR_BIO = "Clinical-stage sponsor — biologics"
SPONSOR_OLIGO = "Clinical-stage sponsor — oligo / peptide"
CLIN_CRO = "Full-service clinical CRO (subcontracts bioanalysis)"
PHARMA = "Large pharma — outsources overflow"
PRECLIN = "Preclinical sponsor (IND within ~12 months)"
INHOUSE = "Sponsor with in-house regulated lab"
IIT = "Academic medical center (investigator-initiated trials)"
CENTRAL = "Central lab"
DX = "Biomarker / diagnostics company"
CONSULT = "Clinical pharmacology / regulatory consultancy"
VENDOR = "Instrument & reagent vendor"
COMPETITOR = "Bioanalytical CRO (competitor)"
REG = "Regulator / standards body"
INVESTOR = "Investor"
TOOLS = "Discovery-only / research tools"
ANIMAL = "Animal health"

# (company, tier, priority, segment, spotlight, signals, why, crm, deal, borderline_note)
CO = [
 # ---- A1: clinical-stage sponsors without a regulated lab ----
 ("Quillfern Therapeutics","A",1,SPONSOR_BIO,"strong","Ph1 active · 2 trials; US sites; ADA required; No in-house regulated lab",
  "Two antibodies in Ph1 at US sites and no regulated bioanalysis lab — PK and ADA testing must be outsourced","Y","Open: ADA method transfer",""),
 ("Saltmarsh Pharmaceuticals","A",1,SPONSOR_SM,"","Ph2 active · 1 trial; LC-MS/MS PK; US sites; No in-house regulated lab",
  "Small molecule in a Ph2 dose-ranging study; PK samples need validated LC-MS/MS","N","",""),
 ("Tidewren Therapeutics","A",1,SPONSOR_OLIGO,"partial","Ph1 active · 1 trial; Hybrid LBA/LC-MS; ADA required",
  "Antisense oligo in Ph1 — needs hybrid PK methods plus immunogenicity","N","",""),
 ("Corvane Biosciences","A",1,SPONSOR_BIO,"strong","Ph2 active · 4 trials; ADA + NAb required; US sites",
  "Four Ph2 trials of a fusion protein; ADA and neutralising-antibody testing across sites","N","",""),
 ("Emberlyne Bio","A",1,SPONSOR_SM,"","Ph1 started this quarter; LC-MS/MS PK; No in-house regulated lab",
  "First-in-human began this quarter; small team, outsources all clinical lab work","Y","",""),
 ("Halvard Immunotherapies","A",1,SPONSOR_BIO,"strong","Ph1 active · 1 trial; ADA required; Uses FSP model; No in-house regulated lab",
  "Bispecific in Ph1; runs studies through a functional service provider — bioanalysis chosen separately","N","",""),
 ("Brindlecove Therapeutics","A",1,SPONSOR_OLIGO,"partial","Ph2 active · 2 trials; Hybrid LBA/LC-MS",
  "siRNA program in Ph2; hybrid LC-MS methods for the conjugate","N","",""),
 ("Ostrander Bio","A",1,SPONSOR_SM,"","Ph1 active · 1 trial; Ph2 active · 1 trial; LC-MS/MS PK; Metabolite ID",
  "Two small-molecule trials, including a food-effect study; metabolite work likely","Y","Closed lost (turnaround time) — warm re-entry",""),
 ("Mirefield Therapeutics","A",1,SPONSOR_BIO,"partial","Ph1 active · 1 trial; ADA required; Hiring bioanalytical scientists",
  "Antibody in Ph1 with ADA needs","N","","Recent job postings for regulated bioanalysis scientists — they may be building an in-house lab"),
 ("Larchmere Biologics","A",1,SPONSOR_BIO,"strong","Ph2 active · 1 trial; Rare disease (small n); ADA + NAb required",
  "Enzyme replacement therapy in Ph2; immunogenicity is a central safety question","N","",""),
 ("Sundry Point Therapeutics","A",1,SPONSOR_SM,"","Ph2 active · 3 trials; LC-MS/MS PK; US sites",
  "Three Ph2 trials of a small molecule; high sample volume","Y","",""),
 ("Harrowgate Bio","A",1,SPONSOR_OLIGO,"","Ph1 active · 1 trial; Peptide PK; No in-house regulated lab",
  "Peptide therapeutic in Ph1; LC-MS/MS PK for a peptide","N","",""),
 ("Oakhollow Therapeutics","A",1,SPONSOR_BIO,"partial","Ph1 active · 1 trial; Sites outside the US only; ADA required",
  "Antibody in Ph1 with ADA needs","N","","All trial sites are outside the US — sample logistics to a US lab may not work"),
 ("Thistledown Bio","A",1,SPONSOR_SM,"","Ph1 active · 1 trial; LC-MS/MS PK; Drug-interaction study planned",
  "Small molecule in Ph1 with a drug-interaction study announced","N","",""),
 ("Seaholm Biologics","A",1,SPONSOR_BIO,"strong","Ph1 active · 2 trials; ADA required; US sites",
  "Two engineered-cytokine trials in Ph1; immunogenicity monitoring required","N","",""),
 # ---- A2: clinical CROs that buy bioanalysis as a subcontract ----
 ("Ridgeline Clinical Research","A",2,CLIN_CRO,"","No in-house regulated lab; Specialty-lab vendor program",
  "Full-service clinical CRO without its own bioanalysis lab; selects specialty-lab subcontractors for sponsor studies","Y","",""),
 ("Halcyon Trial Partners","A",2,CLIN_CRO,"","Specialty-lab vendor program",
  "Early-phase clinical CRO that subcontracts PK and ADA testing","N","","Acquired a small lab last year — may now compete for some of this work"),
 ("Lattice Clinical","A",2,CLIN_CRO,"","No in-house regulated lab",
  "Mid-size clinical CRO; bioanalysis always subcontracted","N","",""),
 # ---- B: large pharma (preferred-vendor lists, long qualification) ----
 ("Grand Meridian Pharma","B",0,PHARMA,"partial","In-house regulated lab; Outsources overflow; Preferred-vendor list; ADA required",
  "Top-20 pharma with in-house labs and a preferred-vendor list for overflow PK and ADA work","Y","Open: overflow ADA testing",""),
 ("Aldermoor Pharmaceuticals","B",0,PHARMA,"","In-house regulated lab; Outsources overflow",
  "Large pharma; outsources roughly a third of clinical PK","N","",""),
 ("Kestrel Hill Pharma","B",0,PHARMA,"partial","In-house regulated lab; Outsources overflow",
  "Large pharma outsourcing exploratory biomarker work","N","",""),
 # ---- B ----
 ("Fernhollow Bio","B",0,PRECLIN,"","IND planned; GLP tox ongoing",
  "Preclinical; will need clinical bioanalysis within a year","N","","IND announced for next quarter — move to A once filed"),
 ("Cindermoss Bio","B",0,PRECLIN,"partial","IND-enabling; ADA required?",
  "IND-enabling antibody program; timing to first-in-human unclear","N","","Press release hints at a first-in-human date — if confirmed, tier A"),
 ("Velloway Bio","B",0,PRECLIN,"","IND-enabling; LC-MS/MS PK",
  "Small molecule in IND-enabling studies","N","",""),
 ("Gullbrook Biosciences","B",0,PRECLIN,"","IND-enabling",
  "Peptide program in IND-enabling studies","N","",""),
 ("Stonebridge Biotherapeutics","B",0,INHOUSE,"partial","In-house regulated lab; Ph3 active · 1 trial",
  "Runs its own regulated bioanalysis lab; outsources only niche assays","Y","",""),
 ("Pinecrest Pharma","B",0,INHOUSE,"","In-house regulated lab; Ph2 active · 2 trials",
  "Mid-size sponsor with a GLP bioanalysis group","N","",""),
 ("Eastmoor University Medical Center","B",0,IIT,"","Investigator-initiated trials",
  "Runs investigator-initiated trials; some need regulated PK","N","",""),
 ("Carrow Cancer Institute","B",0,IIT,"","Investigator-initiated trials",
  "Academic oncology trials with exploratory biomarkers","N","",""),
 # ---- C ----
 ("Northbank Central Laboratories","C",0,CENTRAL,"","Refers specialty testing",
  "Global central lab for safety labs; refers specialty bioanalysis","Y","",""),
 ("Cobblestone Clinical Labs","C",0,CENTRAL,"","Refers specialty testing?",
  "Central lab — partner for kit-building and logistics","N","",""),
 ("Tarnwell Central Lab Services","C",0,CENTRAL,"","Refers specialty testing?",
  "Regional central lab","N","",""),
 ("Tamberlane Diagnostics","C",0,DX,"","Co-marketing potential",
  "Diagnostics company — co-development and referral partner","N","",""),
 ("Cairnhill Clinical Pharmacology Advisors","C",0,CONSULT,"","Refers specialty testing",
  "Consultants who recommend bioanalysis vendors to small sponsors","Y","",""),
 ("Lattice & Vine Regulatory","C",0,CONSULT,"","",
  "Regulatory consultancy","N","",""),
 ("Pellham Instruments","C",0,VENDOR,"","Co-marketing potential",
  "Instrument vendor — application-note and co-marketing partner","N","",""),
 ("Wrenfield Reagents","C",0,VENDOR,"","Co-marketing potential",
  "Assay reagent supplier","N","",""),
 # ---- X ----
 ("Plinthwell Analytical","X",0,COMPETITOR,"","Competitor",
  "Direct competitor: regulated PK and immunogenicity","N","",""),
 ("Ferncastle Bioanalytics","X",0,COMPETITOR,"","Competitor",
  "Direct competitor","N","",""),
 ("Kittering Analytical","X",0,COMPETITOR,"","Competitor",
  "Direct competitor","N","",""),
 ("Matrix & Method Labs","X",0,COMPETITOR,"","Competitor",
  "Competitor in biomarker assays","N","",""),
 ("National Drug Review Agency","X",0,REG,"","Regulator — listen, don't pitch",
  "Fictional regulator — relationship and learning, never a sales conversation","N","",""),
 ("Bioanalysis Standards Consortium","X",0,REG,"","Regulator — listen, don't pitch",
  "Industry standards group","N","",""),
 ("Juniper Rock Ventures","X",0,INVESTOR,"","","Venture investor","N","",""),
 ("Morrow Street Capital","X",0,INVESTOR,"","","Life-science fund","N","",""),
 ("Lumen Discovery Tools","X",0,TOOLS,"","No clinical programs","Discovery assay kits; no clinical work","N","",""),
 ("Copperleaf Screening","X",0,TOOLS,"","No clinical programs","High-throughput screening services","N","",""),
 ("Bramblegate Bio","X",0,TOOLS,"","No clinical programs; IND-enabling?",
  "Discovery-stage only","N","","Pipeline page now lists an IND-enabling program — may belong in B"),
 ("Fennick Animal Health","X",0,ANIMAL,"","No clinical programs","Animal-health only — outside our regulated scope","N","",""),
]

FIRST = """Ava Ben Chiara Dev Elena Farid Grace Hiro Imani Jonas Kavya Liam Mei Nadia Omar Priya Quentin Rosa
Samir Tara Umar Vera Wesley Xin Yara Zane Aisha Bruno Camille Dario Esme Felix Greta Hassan Ines Jamal Keiko Lars
Marisol Nikhil Olga Pavel Rhea Soren Tomas Uma Viktor Wren Yusuf Zara Ana Theo Lena Mateo Noor Ravi Sofia Kofi""".split()
LAST = """Abernethy Bauer Castellanos Dmitrov Eklund Faraday Gallo Hartwell Ibarra Jansen Kowalczyk Lindgren Moreau
Nakamura Okafor Pellegrini Quist Rasmussen Sandoval Thorne Ulrich Vasquez Whitlock Xu Yamada Zielinski Achterberg
Brennan Coelho Delacroix Engstrom Fairweather Gunnarsson Holloway Iwasaki Jovanovic Kerrigan Laurent Mbeki Novak
Oyelaran Pacheco Renner Sato Takahashi Underwood Valdivia Westbrook Ylvisaker Zorrilla Haddad Mensah Ferreira Lund""".split()

E, D, S, M, J = "Exec / VP+", "Director", "Senior IC", "Manager / IC", "Junior / IC"
BA, CP, IM, BM, OUT, OPS, LAB, QA, BD, LEAD, OTH = ("Bioanalytical / DMPK", "Clinical pharmacology", "Immunogenicity",
    "Biomarker / translational", "Clinical outsourcing", "Clinical operations", "Lab operations", "QA / GLP",
    "BD / commercial", "Leadership", "Other")
T_SPONSOR = [
 ("Chief Medical Officer",E,LEAD),("Director, Bioanalytical Sciences",D,BA),("Head of Clinical Pharmacology",E,CP),
 ("Director, Clinical Outsourcing",D,OUT),("Associate Director, Immunogenicity",D,IM),("Principal Scientist, Bioanalysis",S,BA),
 ("Clinical Pharmacologist",S,CP),("Director, Clinical Operations",D,OPS),("Senior Scientist, Biomarkers",S,BM),
 ("Director, DMPK",D,BA),("Senior Manager, Vendor Management",M,OUT),("Clinical Trial Manager",M,OPS),
 ("QA Manager, GxP",M,QA),("Research Associate",J,LAB),("VP, Clinical Development",E,LEAD),("Head of Translational Medicine",E,BM),
 ("Director, Clinical & Commercial Drug Supply",D,OPS),("Program Lead",("Other / unclear"),OTH),
]
T_CLINCRO = [("Director, Laboratory Vendor Management",D,OUT),("Associate Director, Specialty Labs",D,LAB),
 ("Project Director",D,OPS),("VP, Business Development",E,BD),("Senior Manager, Sample Management",M,LAB),
 ("Clinical Research Associate",J,OPS),("Head of Early-Phase Operations",E,OPS)]
T_PHARMA = [("Director, External Bioanalysis",D,OUT),("Senior Scientist, Regulated Bioanalysis",S,BA),
 ("Executive Director, DMPK",E,BA),("Principal Scientist, Immunogenicity",S,IM),("Associate Director, Clinical Pharmacology",D,CP),
 ("Scientist II, Bioanalysis",M,BA),("Senior Manager, Strategic Sourcing — Labs",M,OUT),("Director, Biomarker Operations",D,BM)]
T_COMP = [("Study Director, GLP",S,LAB),("Principal Scientist, Ligand Binding",S,BA),("Director, Business Development",D,BD),
 ("Lab Manager",M,LAB),("Senior Scientist, LC-MS/MS",S,BA),("Account Executive",M,BD)]
T_CENTRAL = [("Director, Partnerships",D,BD),("Head of Specialty Testing",E,LAB),("Account Manager",M,BD),("Senior Project Manager",M,OPS)]
T_CONSULT = [("Principal Consultant",("Consultant"),CP),("Founder & Managing Partner",("Consultant"),LEAD),("Senior Regulatory Advisor",("Consultant"),QA)]
T_VENDOR = [("Applications Scientist",S,OTH),("Regional Sales Manager",M,BD),("Product Manager, Bioanalysis",M,BD)]
T_IIT = [("Director, Clinical Research Program",D,OPS),("Professor of Clinical Pharmacology",("Academic"),CP),
 ("Research Coordinator",J,OPS),("Translational Research Scientist",("Academic"),BM)]
T_REG = [("Reviewer, Office of Clinical Pharmacology",("Other / unclear"),OTH),("Senior Policy Advisor",("Other / unclear"),OTH)]
T_INV = [("Partner",E,OTH),("Principal",("Other / unclear"),OTH),("Associate",J,OTH)]
T_TOOLS = [("CEO",E,LEAD),("Field Application Scientist",S,OTH),("Sales Director",D,BD)]

def pool(seg):
    return {CLIN_CRO: T_CLINCRO, PHARMA: T_PHARMA, COMPETITOR: T_COMP, CENTRAL: T_CENTRAL, CONSULT: T_CONSULT,
            VENDOR: T_VENDOR, IIT: T_IIT, REG: T_REG, INVESTOR: T_INV, TOOLS: T_TOOLS, ANIMAL: T_TOOLS, DX: T_CENTRAL}.get(seg, T_SPONSOR)

def ncount(tier, prio, seg):
    if seg == COMPETITOR: return random.randint(6, 12)   # a regulated-bioanalysis workshop is competitor-heavy
    if seg == PHARMA: return random.randint(8, 13)
    return {"A": random.randint(3, 7), "B": random.randint(2, 5), "C": random.randint(2, 5), "X": random.randint(2, 6)}[tier]

def domain(co):
    return "".join(ch for ch in co.lower().split()[0] if ch.isalpha()) + ".example"

SENIOR = {E, D, S}
SPONSOR_FUN = {BA, CP, IM, BM, OUT}
SPONSORS = {SPONSOR_SM, SPONSOR_BIO, SPONSOR_OLIGO}

def recommended(tier, seg, spot, sen, fun):
    """The example rubric's preselect rule, which differs by segment."""
    if tier == "A" and seg in SPONSORS:
        return (sen in SENIOR and fun in SPONSOR_FUN) or (fun in {OPS, LEAD} and sen in {E, D})
    if tier == "A" and seg == CLIN_CRO:
        return sen in {E, D} and fun in {OUT, LAB, OPS}
    if spot == "strong":
        return sen in SENIOR and fun not in {BD, OTH}
    return False

used = set()
def person():
    while True:
        n = f"{random.choice(FIRST)} {random.choice(LAST)}"
        if n not in used:
            used.add(n); return n

raw, scored, pid = [], [], 0
def add(co, t, sen, fun, badge=None, note=""):
    global pid
    (name, tier, prio, seg, spot, sig, why, crm, deal, bnote) = co
    pid += 1
    nm = person()
    rec = "Y" if recommended(tier, seg, spot, sen, fun) else ""
    scored.append({"PersonId": f"p{pid:04d}", "Name": nm, "Title": t, "Company": name, "BadgeCompany": badge or name,
                   "Tier": tier, "TierName": TIER_NAMES[tier], "Priority": prio or "", "Segment": seg, "Spotlight": spot,
                   "Signals": sig, "Why": why, "Borderline": "Y" if bnote else "", "BorderlineNote": bnote,
                   "Seniority": sen, "Function": fun, "Recommended": rec, "CRMAccount": crm, "CRMDeal": deal, "Note": note})
    raw.append({"Name": nm, "Title": t, "Company": badge or name})
    return scored[-1]

for co in CO:
    titles = pool(co[3])
    for i in range(ncount(co[1], co[2], co[3])):
        t, sen, fun = titles[i] if i < min(len(titles), 3) else random.choice(titles)
        add(co, t, sen, fun)

# Same person under a former company name — flag, never merge
ost = next(c for c in CO if c[0] == "Ostrander Bio")
first = next(r for r in scored if r["Company"] == "Ostrander Bio" and r["Recommended"] == "Y")
pid += 1
scored.append({**first, "PersonId": f"p{pid:04d}", "BadgeCompany": "Ostrander Pharmaceuticals (former name)",
               "Note": f"Same person as {first['PersonId']} — badge shows the company's former name"})
raw.append({"Name": first["Name"], "Title": first["Title"], "Company": "Ostrander Pharmaceuticals"})
# Raw-list quirks for prepare_list.py: an exact duplicate and a look-alike period (U+2024)
raw.append(dict(raw[3]))
per = next(c for c in CO if c[0] == "Larchmere Biologics")
r = add(per, "Associate Director, Immunogenicity", D, IM, badge="Larchmere Biologics Inc.")
raw[-1]["Name"] = "Dr․ " + r["Name"]
random.shuffle(raw)

def write(name, rows, fields, bom=False):
    with open(os.path.join(OUTDIR, name), "w", newline="", encoding="utf-8-sig" if bom else "utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

write("attendees.csv", raw, ["Name", "Title", "Company"], bom=True)
write("scored.csv", scored, list(scored[0].keys()))

crm_rows = [{"Company": c[0], "Domain": domain(c[0]), "Deal": c[8]} for c in CO if c[7] == "Y"]
write("crm-companies.csv", crm_rows, ["Company", "Domain", "Deal"])
contacts = []
for r in scored:
    if r["CRMAccount"] == "Y" and random.random() < 0.3 and not r["Note"]:
        f_, l_ = r["Name"].split(" ", 1)
        contacts.append({"Name": r["Name"], "Company": r["Company"], "Email": f"{f_.lower()}.{l_.lower()}@{domain(r['Company'])}"})
write("crm-contacts.csv", contacts, ["Name", "Company", "Email"])

# ---- Stage 2 demo: research a spread of the recommended shortlist ----
recs = [r for r in scored if r["Recommended"] == "Y" and not r["Note"]]
by_co = {}
for r in recs:
    by_co.setdefault(r["Company"], []).append(r)
short, rnd = [], 0
while len(short) < 40 and rnd < 3:
    for v in by_co.values():
        if rnd == 0: random.shuffle(v)
        if len(v) > rnd and len(short) < 40:
            short.append(v[rnd])
    rnd += 1
for fun in (IM, OUT, CP, BM):  # make sure the demo shows every key function at least once
    if not any(x["Function"] == fun for x in short):
        extra = next((x for x in recs if x["Function"] == fun and x not in short), None)
        if extra:
            short[-1 if len(short) >= 40 else len(short):] = [extra]
short.sort(key=lambda r: r["Company"])
contact_by = {c["Name"]: c["Email"] for c in contacts}

FOCUS = {BA: "Owns regulated PK methods and external bioanalysis for the clinical programs",
         CP: "Leads clinical pharmacology and PK strategy for early trials",
         IM: "Runs the immunogenicity (ADA/NAb) strategy for the lead biologic",
         BM: "Leads biomarker and translational sample work",
         OUT: "Selects and oversees clinical lab vendors",
         OPS: "Runs trial operations, including lab and sample logistics",
         LAB: "Manages specialty-lab subcontractors across sponsor studies",
         LEAD: "Sets clinical development direction"}
H1 = {BA: ["Presented a poster on validating an LC-MS/MS PK method under harmonised bioanalytical guidance (workshop abstract book)",
           "Listed as bioanalytical contact in the company's Ph1 publication"],
      CP: ["Listed as clinical pharmacology lead on the trial-registry entry for the Ph1 study",
           "Co-author of a population-PK abstract for the lead asset"],
      IM: ["Authored a tiered ADA strategy poster for the company's lead biologic",
           "Joined from a large-pharma immunogenicity group this year"],
      BM: ["Recent talk on fit-for-purpose biomarker validation for a Ph2 program"],
      OUT: ["Owns specialty-lab vendor selection (per a job posting they authored)",
            "Spoke on vendor oversight for small sponsors at a regional meeting"],
      OPS: ["Manages the company's US Ph1 sites; quoted in a site-activation press release"],
      LAB: ["Runs the specialty-lab subcontractor program across sponsor studies"],
      LEAD: ["Took the lead asset into first-in-human", "Co-founder; previously ran clinical pharmacology at a mid-size pharma"]}
H2 = ["Previously worked in a regulated bioanalysis lab at a large CRO", "Background in DMPK before moving into clinical development",
      "Publishes on immunogenicity risk assessment", "Prior role managing central-lab vendors"]
PRIOR = ["A large CRO's bioanalytical lab", "A large-pharma DMPK group", "A central laboratory", "An academic clinical pharmacology unit"]
research = []
for i, r in enumerate(short):
    conf = ["high", "medium", "unsure"][(i * 7) % 3] if i % 5 else "high"
    if conf == "unsure":
        focus = h1 = h2 = ten = prior = ""
    else:
        focus = FOCUS.get(r["Function"], "Works on the clinical programs")
        opts = H1.get(r["Function"], ["Works on the company's clinical programs"])
        h1 = opts[i % len(opts)]
        h2 = "" if conf == "medium" else H2[i % len(H2)]
        yrs = 1 + (i % 6)
        ten = f"{yrs} yr{'s' if yrs > 1 else ''} in role"
        prior = "" if conf == "medium" else PRIOR[i % len(PRIOR)]
    email, basis = (contact_by[r["Name"]], "crm") if r["Name"] in contact_by else ("", "none")
    research.append({"Name": r["Name"], "Title": r["Title"], "Company": r["Company"], "Tier": r["Tier"],
                     "Segment": r["Segment"], "Seniority": r["Seniority"], "Function": r["Function"],
                     "Confidence": conf, "Focus": focus, "Highlight1": h1, "Highlight2": h2, "Tenure": ten, "Prior": prior,
                     "ScopeWarning": "", "Email": email, "EmailBasis": basis, "Speaker": "", "TitleMismatch": "", "Sources": ""})
def pick(fun):
    x = next((x for x in research if x["Function"] == fun and x["Confidence"] != "unsure"), None) \
        or next(x for x in research if x["Function"] == fun)
    if x["Confidence"] == "unsure":  # a confirmed speaker is at least medium confidence
        x.update(Confidence="medium", Focus=FOCUS[fun], Highlight1=H1[fun][0], Tenure="2 yrs in role")
    return x
spk1, spk2 = pick(IM), pick(OUT)
spk1["Speaker"] = "Day 1 · 10:30 · Hall B — Tiered ADA assays: setting cut points for small clinical studies"
spk2["Speaker"] = "Day 2 · 14:00 · Room 3 — Panel: choosing and overseeing specialty-lab vendors"
spk2["TitleMismatch"] = f"Agenda lists them as VP, Clinical Outsourcing; badge says {spk2['Title']}"
warn = next((x for x in research if x["Confidence"] == "medium" and x["Function"] == BA and not x["Speaker"]), None) or next(x for x in research if x["Confidence"] == "medium" and not x["Speaker"])
warn["ScopeWarning"] = "Recent talks are about discovery-stage screening only — check they touch the clinical programs"
write("research.csv", research, list(research[0].keys()))

with open(os.path.join(OUTDIR, "agenda.md"), "w") as f:
    f.write(f"""# {EVENT} — agenda excerpt (fictional)

## Day 1

**10:30 · Hall B — Tiered ADA assays: setting cut points for small clinical studies**
{spk1['Name']}, {spk1['Title']}, {spk1['Company']}

**13:15 · Room 2 — Keynote: one year of harmonised bioanalytical guidance**
Fictional speaker, National Drug Review Agency

**16:00 · Poster hall — Hybrid LBA/LC-MS methods for oligonucleotides**
Poster session

## Day 2

**14:00 · Room 3 — Panel: choosing and overseeing specialty-lab vendors**
{spk2['Name']}, VP, Clinical Outsourcing, {spk2['Company']}
Panelist from Cairnhill Clinical Pharmacology Advisors
""")

overrides = [
 {"Company": "Northbank Central Laboratories", "Segment": CENTRAL, "AITier": "C", "YourTier": "X", "Reason": "At this workshop central labs are exhibiting specialty bioanalysis — they're competing, not referring", "Scope": "event"},
 {"Company": "Cobblestone Clinical Labs", "Segment": CENTRAL, "AITier": "C", "YourTier": "X", "Reason": "Booth lists PK and ADA testing", "Scope": "event"},
 {"Company": "Tarnwell Central Lab Services", "Segment": CENTRAL, "AITier": "C", "YourTier": "X", "Reason": "Same — pitching bioanalysis here", "Scope": "event"},
 {"Company": "Cindermoss Bio", "Segment": PRECLIN, "AITier": "B", "YourTier": "A", "Reason": "Press release confirms first-in-human in Q1", "Scope": ""},
 {"Company": "Velloway Bio", "Segment": PRECLIN, "AITier": "B", "YourTier": "A", "Reason": "IND filed last month", "Scope": ""},
 {"Company": "Eastmoor University Medical Center", "Segment": IIT, "AITier": "B", "YourTier": "X", "Reason": "Investigator-initiated trials almost never fund regulated bioanalysis", "Scope": "core"},
 {"Company": "Halcyon Trial Partners", "Segment": CLIN_CRO, "AITier": "A", "YourTier": "A", "Reason": "Their acquired lab only runs safety labs — still a buyer", "Scope": ""},
]
write("overrides-example.csv", overrides, ["Company", "Segment", "AITier", "YourTier", "Reason", "Scope"])

from collections import Counter
print("people:", len(scored), "companies:", len(CO), "tiers:", Counter(r["Tier"] for r in scored),
      "recommended:", sum(r["Recommended"] == "Y" for r in scored), "research:", len(research),
      Counter(r["Confidence"] for r in research), "contacts:", len(contacts))
