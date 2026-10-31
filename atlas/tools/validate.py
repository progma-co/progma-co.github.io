"""Checks atlas/data before a change goes live. Run: python atlas/tools/validate.py"""
import json, glob, re, sys, os
root = os.path.join(os.path.dirname(__file__), "..", "data")
errs = []
def load(p):
    try: return json.load(open(p, encoding="utf-8"))
    except Exception as e: errs.append(f"{p}: not valid JSON ({e})"); return {}
tax = load(f"{root}/taxonomy.json")
segs = {s["id"]: n["id"] for n in tax.get("nodes", []) for s in n["subsegments"]}
layers = {l["id"] for l in tax.get("layers", [])}
for n in tax.get("nodes", []):
    for s in n["subsegments"]:
        if s.get("layer") not in layers: errs.append(f"taxonomy: {s['id']} has unknown layer {s.get('layer')}")
KINDS = {"company", "open-source project", "open-weight model", "standard", "open dataset", "public programme"}
REGIONS = {"North America", "Europe", "China", "India", "Asia-Pacific", "Middle East", "Latin America", "Africa"}
STAGES = {"Pre-seed/Seed", "Series A", "Series B", "Series C+"}
seen = {}
for f in sorted(glob.glob(f"{root}/nodes/*.json")):
    d = load(f); nid = os.path.basename(f)[:-5]
    for i, e in enumerate(d.get("entries", [])):
        where = f"{os.path.basename(f)} #{i} ({e.get('name', '?')})"
        for req in ("name", "kind", "subsegments", "one_liner", "url"):
            if not e.get(req): errs.append(f"{where}: missing {req}")
        if e.get("kind") not in KINDS: errs.append(f"{where}: kind must be one of {sorted(KINDS)}")
        bad = [s for s in e.get("subsegments", []) if s not in segs]
        if bad: errs.append(f"{where}: unknown sub-segment ids {bad}")
        elif e.get("subsegments") and segs[e["subsegments"][0]] != nid: errs.append(f"{where}: first sub-segment belongs to {segs[e['subsegments'][0]]}, so the entry belongs in nodes/{segs[e['subsegments'][0]]}.json")
        if e.get("region") and e["region"] not in REGIONS: errs.append(f"{where}: region must be one of {sorted(REGIONS)}")
        if e.get("stage") and e["stage"] not in STAGES: errs.append(f"{where}: stage must be one of {sorted(STAGES)}")
        for u in ("url", "source", "repo", "round_source"):
            if e.get(u) and not re.match(r"https?://", e[u]): errs.append(f"{where}: {u} must be a full http(s) link")
        if len(e.get("one_liner", "").split()) > 25: errs.append(f"{where}: one_liner over 25 words")
        k = re.sub(r"[^a-z0-9]", "", e.get("name", "").lower())
        if k in seen: errs.append(f"{where}: duplicate of {seen[k]} (list it once with several sub-segments)")
        seen[k] = where
for f, key in (("cross.json", "cross"), ("investors.json", "investors")):
    for x in load(f"{root}/{f}").get(key, []):
        for r in x.get("roles", []):
            if r.get("subsegment") not in segs: errs.append(f"{f}: {x.get('name')} has unknown sub-segment {r.get('subsegment')}")
if errs:
    print(f"{len(errs)} problem(s):"); [print(" -", e) for e in errs[:200]]; sys.exit(1)
print(f"OK: {len(seen)} entries across {len(segs)} sub-segments")
