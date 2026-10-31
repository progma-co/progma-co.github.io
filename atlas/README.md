# AI Value Chain Atlas

Live at **https://www.progma.co.in/atlas/** · maintained by [Progma](https://www.progma.co.in) · data licensed CC BY 4.0

Who does what across the AI value chain, from power and silicon through models, inference and tooling to applications, services and users. Columns are the 12 value-chain nodes; rows are the five support layers around each node (core offering, critical inputs, optimisation, ops & governance, distribution).

## How to contribute

| You want to | Do this |
|---|---|
| Add a company, open project or investor | [Open an "add" issue](../../../issues/new?template=atlas-suggest.yml) |
| Fix something wrong or outdated | [Open a "correction" issue](../../../issues/new?template=atlas-correct.yml) |
| Keep your company's listing accurate | [Claim it](../../../issues/new?template=atlas-claim.yml) from your organisation's GitHub account |
| Share the stack you run on | Use **Build my stack** on the page, then **Submit to gallery** |
| Edit the data directly | Edit the right file in `atlas/data/nodes/` and open a pull request |

Every change needs a source link and is reviewed before it goes live. Listings are never paid for. Representing the company you add is fine; say so in the form.

## Data layout

```
atlas/data/
  taxonomy.json        nodes, sub-segments, layers, transitions
  nodes/n0.json … n11.json   one file per node: {"entries": [...], "notes": {...}}
  cross.json           companies that span several nodes, with what they offer in each box
  investors.json       investors and the boxes their AI portfolio sits in
  stacks.json          community stacks
  meta.json            update date, buyer personas, changelog
```

An entry lives in the file of the node of its **first** sub-segment, and is listed once with all its sub-segments. Fields:

| Field | Required | Notes |
|---|---|---|
| `name` | yes | As commonly known |
| `kind` | yes | `company`, `open-source project`, `open-weight model`, `standard`, `open dataset`, `public programme` |
| `subsegments` | yes | Ids from `taxonomy.json`, e.g. `n7.route` |
| `one_liner` | yes | What it sells or does, factual, 20 words or fewer |
| `url` | yes | Official site or repo |
| `source` | yes for changes | Link that backs the latest fact |
| `hq`, `region` | companies | ISO country code; region from the fixed list |
| `status`, `parent` | companies | `public`, `private`, `acquired` (+ acquirer) |
| `stage`, `last_round`, `round_source` | optional | Latest disclosed round only |
| `licence`, `access`, `repo`, `steward` | open entries | Licence as published; how someone actually gets it |
| `tags` | optional | `performance`, `cost`, `open-source`, `sovereign`, `security`, `enterprise`, `developer` |

Run `python atlas/tools/validate.py` before opening a pull request; the same check runs automatically.

## Update rhythm

Every fortnight (1st and 15th) the atlas is re-scanned: new issues and suggestions, market moves (acquisitions, launches, shutdowns, funding), and a rotating re-check of older listings. Changes arrive as one reviewed pull request with a changelog entry.

## Licence

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it, fork it, build on it; credit "Progma AI Value Chain Atlas" with a link to https://www.progma.co.in/atlas/.
