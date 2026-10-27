#!/usr/bin/env python3
"""Clean a raw people list and (optionally) match it against a CRM export.

Usage:
  python3 prepare_list.py attendees.csv [--crm crm-companies.csv] [--aliases aliases.csv] [-o prepared.csv]

Input columns are matched case-insensitively; common variants are accepted
(e.g. "Full Name", "Job Title", "Organization"). The CRM export needs a company
column and may have "Domain" and "Deal" columns. An aliases file has two columns:
"SeenAs","TreatAs".

Output adds: CompanyKey, CRMAccount (Y/blank), CRMMatch (exact / candidate / blank),
CRMCompany, CRMDeal, DuplicateOf. "candidate" matches are suggestions for the AI or
the user to confirm by domain — they are never treated as confirmed.
Standard library only.
"""
import argparse, csv, re, sys, unicodedata

SUFFIXES = r"(incorporated|inc|llc|ltd|limited|plc|gmbh|ag|sa|sas|bv|nv|ab|as|oy|kk|co|corp|corporation|company|" \
           r"group|holdings|pharmaceuticals?|pharma|therapeutics|biotherapeutics|biosciences?|biologics|" \
           r"biotech(nology)?|bio|labs?|laboratories)"
NAME_COLS = ["name", "full name", "fullname", "attendee", "person"]
FIRST_COLS = ["first name", "firstname", "given name"]
LAST_COLS = ["last name", "lastname", "surname", "family name"]
TITLE_COLS = ["title", "job title", "jobtitle", "position", "role"]
COMPANY_COLS = ["company", "organization", "organisation", "org", "employer", "account", "company name"]


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def key(company, aliases=None):
    c = norm(company).lower()
    if aliases and c in aliases:
        c = aliases[c]
    c = c.replace("&", " and ")
    c = re.sub(r"[^\w\s]", " ", c)
    words = c.split()
    while words and re.fullmatch(SUFFIXES, words[-1]):
        words.pop()
    return " ".join(words) or c.strip()


def pick(header, options):
    low = {h.lower().strip(): h for h in header}
    for o in options:
        if o in low:
            return low[o]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--crm")
    ap.add_argument("--aliases")
    ap.add_argument("-o", "--output", default="prepared.csv")
    a = ap.parse_args()

    aliases = {}
    if a.aliases:
        with open(a.aliases, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                vals = list(r.values())
                if len(vals) >= 2 and vals[0]:
                    aliases[norm(vals[0]).lower()] = norm(vals[1]).lower()

    with open(a.input, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        hdr = rd.fieldnames or []
        rows = list(rd)
    ncol, tcol, ccol = pick(hdr, NAME_COLS), pick(hdr, TITLE_COLS), pick(hdr, COMPANY_COLS)
    fcol, lcol = pick(hdr, FIRST_COLS), pick(hdr, LAST_COLS)
    if not ccol or not (ncol or (fcol and lcol)):
        sys.exit(f"Couldn't find name/company columns in: {hdr}")

    crm = []
    if a.crm:
        with open(a.crm, encoding="utf-8-sig", newline="") as f:
            rd = csv.DictReader(f)
            cc = pick(rd.fieldnames, COMPANY_COLS)
            dc = pick(rd.fieldnames, ["domain", "website"])
            dl = pick(rd.fieldnames, ["deal", "deals", "open deal", "deal stage"])
            for r in rd:
                crm.append({"name": norm(r[cc]), "key": key(r[cc], aliases),
                            "domain": norm(r.get(dc, "")) if dc else "", "deal": norm(r.get(dl, "")) if dl else ""})
    crm_by_key = {c["key"]: c for c in crm}

    out, seen = [], {}
    for r in rows:
        name = norm(r[ncol]) if ncol else norm(f"{r[fcol]} {r[lcol]}")
        name = re.sub(r"^(dr|prof|mr|mrs|ms)\.?\s+", "", name, flags=re.I)
        title, company = norm(r.get(tcol, "") if tcol else ""), norm(r[ccol])
        k = key(company, aliases)
        sig = (name.lower(), title.lower(), k)
        if sig in seen:
            continue  # exact duplicate after normalising
        seen[sig] = len(out)
        rec = {**{h: norm(v) for h, v in r.items() if h}, "Name": name, "Title": title, "Company": company,
               "CompanyKey": k, "CRMAccount": "", "CRMMatch": "", "CRMCompany": "", "CRMDeal": "", "DuplicateOf": ""}
        hit = crm_by_key.get(k)
        if hit:
            rec.update(CRMAccount="Y", CRMMatch="exact", CRMCompany=hit["name"], CRMDeal=hit["deal"])
        elif crm and len(k) >= 5:
            cands = [c for c in crm if len(c["key"]) >= 5 and (k in c["key"] or c["key"] in k)]
            if len(cands) == 1:
                rec.update(CRMMatch="candidate", CRMCompany=cands[0]["name"])
        out.append(rec)

    # Same name under two different companies: flag, never merge
    by_name = {}
    for i, r in enumerate(out):
        by_name.setdefault(r["Name"].lower(), []).append(i)
    for idxs in by_name.values():
        if len({out[i]["CompanyKey"] for i in idxs}) > 1:
            for i in idxs[1:]:
                out[i]["DuplicateOf"] = f"{out[idxs[0]]['Name']} @ {out[idxs[0]]['Company']}"

    fields = list(dict.fromkeys(["Name", "Title", "Company", "CompanyKey", "CRMAccount", "CRMMatch", "CRMCompany",
                                 "CRMDeal", "DuplicateOf"] + [h for h in hdr if h]))
    with open(a.output, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(out)

    comps = {r["CompanyKey"] for r in out}
    print(f"{len(rows)} rows in -> {len(out)} people, {len(comps)} companies "
          f"({len(rows) - len(out)} exact duplicates removed)")
    if crm:
        ex = len({r['CompanyKey'] for r in out if r['CRMMatch'] == 'exact'})
        ca = len({r['CompanyKey'] for r in out if r['CRMMatch'] == 'candidate'})
        print(f"CRM: {ex} companies matched exactly, {ca} candidate matches to confirm by domain")
    dups = sum(1 for r in out if r["DuplicateOf"])
    if dups:
        print(f"{dups} people appear under more than one company — flagged in DuplicateOf, not merged")
    print(f"Wrote {a.output}")


if __name__ == "__main__":
    main()
