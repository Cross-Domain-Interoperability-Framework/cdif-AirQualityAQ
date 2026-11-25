# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

See `README.md` for the full narrative (purpose, provenance, licensing). This file is operational guidance for working in the repo.

## What this repo is

A working repository for an **Air-Quality (AQ) profile of CDIF** for low-cost air-quality sensor (LCS) data. It holds: the source metadata schemas AQ providers use, a crosswalk of their properties onto the CDIF profiles, example CDIF metadata records derived from harvested data, and the controlled vocabularies those records need. There **is** now code here (Python generators under `scripts/`); it is not a git repository.

The `w3id.org/cdif/airquality/…` IRIs in the vocabularies and records are **placeholders — not registered**. Do not treat them as resolvable.

## Layout

- **Source schemas** (Excel, in `docs/`): `docs/LCSmetadata__.xlsx` (original EEA/AAQD-aligned LCS template, author "GSS", unmodified source), `docs/LCSmetadataAnnotated.xlsx` (annotated working copy), `docs/AirGradient_metadata_annotated.xlsx` (AirGradient intake questionnaire; row 1 = schema.org-style property labels, row 2 = questions, rows 3+ = answers).
- **Reference**: `FILTER_ReadMe_DataDescriptor.pdf` (root), `docs/figshare_27195720_metadata.json` (the FILTER PM2.5 dataset: Hassani et al. 2025/NILU, DOI 10.6084/m9.figshare.27195720, CC BY 4.0).
- **Crosswalk**: `AQ_CDIF_profile_mapping.xlsx` — 234 source properties × CDIF profiles. Sheets: `Mapping`, `Gaps (extension schema)`, `Extension concepts`. Status values `mapped`/`partial`/`excluded`.
- **`data_examples/`**: six folders, each with a raw data CSV, (for OpenAQ) the raw `location-*-metadata.json` it came from, and a `*-cdif.jsonld` CDIF record. Three FILTER folders are **wide** CSVs (→ datadescription); three OpenAQ folders are **long/EAV** CSVs (→ datastructure).
- **`vocabularies/`**: six CDIF `skos:ConceptScheme` docs (`pollutant`, `measurement-method`, `station-class`, `mobility`, `qc`, `activity`).
- **`scripts/`**: the generators — `build_mapping_xlsx.py`, `build_instances.py`, `build_vocabularies.py`.

## The CDIF profiles (validation targets) live in sibling repos

The profiles the records/vocabularies validate against are **not in this repo** — they are sibling directories under `C:\GithubC\CDIF\`:
`profile-core`, `profile-discovery`, `profile-datadescription`, `profile-datastructure`, `profile-access`, `profile-codelist`, `profile-conceptscheme`, and the Instrument building block in `metadataBuildingBlocks/_sources/schemaorgProperties/instrument/`. Each profile has a `cdif*StructuredSchema.json` (the JSON Schema used for validation), a `cdif*-frame.jsonld`, SHACL rules, and examples.

## Working with the Excel workbooks

Python with `openpyxl` (`python -I`). Load with `data_only=True` for values; the template sheets report inflated `max_row` (~1000) from formatting, so filter non-empty rows. Load without `read_only` when you need cell fill colour (blue = new element in the LCS template). Some cells have non-UTF-8 chars (`°C`, dashes) that print as `�` — a source artifact, not corruption.

`~$*.xlsx` are Excel lock files: the workbook is open in Excel. **Do not write** to a workbook (or to `AQ_CDIF_profile_mapping.xlsx`) while its lock file exists — `openpyxl.save` raises `PermissionError`. The generators fall back to a `*_reviewed.xlsx` filename on lock.

### LCS template structure (`proposed tables` sheet in docs/LCSmetadataAnnotated.xlsx)

Rows 1–10 = author notes + colour legend. Row 11 = header. The source property names are in **columns A, D, E** (this is the convention used by the crosswalk):

| Col | Meaning |
|---|---|
| A | EEA AQ database / EU 2011/850 equivalent element |
| B | Mandatory under EU legislation (`x`) |
| C | Obligation: `M` mandatory, `Mav` mandatory if available, `V` voluntary |
| D | Identifier / code / link element (`>>>>` = FK to another table; `*` = ID built per the rules sheet) |
| E | Data-point element |
| F | Explanation · G | Examples · I | EEA code-list link |

Relational tables (each starts at a row whose col D holds the table name): Measurement Location → Sampling Point → Sensor Device → Sensing Element → LowCostSensors Deployment → Calibration → LowCostSensors Measurements. Other sheets: `Recommended_Rules_Identifiers` (ID patterns ML_/SP_/SD_/SE_/DEP_/CAL_), `Important Notes` (EEA coords ETRS89/LAEA, EPSG:3035).

## Working with the CDIF records and vocabularies

These are **JSON-LD**. Validate with `jsonschema` against the sibling profile schemas:

```python
import json, jsonschema
schema = json.load(open(r"C:\GithubC\CDIF\profile-discovery\cdifDiscoveryStructuredSchema.json", encoding="utf-8"))
doc    = json.load(open(r"data_examples\CHE_corrected\PA112746-cdif.jsonld", encoding="utf-8"))
print(len(list(jsonschema.Draft202012Validator(schema).iter_errors(doc))), "errors")
```

Which schema per artifact:
- all `*-cdif.jsonld` → `cdifDiscoveryStructuredSchema.json`
- FILTER records (wide) → also `cdifDataDescriptionStructuredSchema.json`
- OpenAQ records (long) → also `cdifDataStructureStructuredSchema.json`
- `vocabularies/*.jsonld` → `cdifConceptSchemeStructuredSchema.json`

Everything currently validates with **0 errors**; keep it that way when editing.

## Regenerating artifacts

The crosswalk, records, and vocabularies are generated by `scripts/`. **Caveat:** the scripts contain **absolute paths** to the sibling CDIF profile repos under `C:\GithubC\CDIF\` and to harvested source files; they are "as-run" provenance, not portable tools. They also each **validate their output** against the profile schemas as they build, and `build_instances.py` **patches the hand-authored** `location-1236012-cdif.jsonld` (AirGradient) in place at the end. Run from anywhere with Python + `openpyxl` + `jsonschema`:

```powershell
python scripts/build_vocabularies.py
python scripts/build_instances.py
python scripts/build_mapping_xlsx.py
```

The AirGradient record (`location-1236012-cdif.jsonld`) is **hand-authored** (it carries richer questionnaire context than the generator produces) and then patched; edit it directly, not via the generator, but re-run `build_instances.py` afterward to re-apply the LongDataStructure patch.

## Gotchas specific to this domain

- **`schema:identifier` encoding** (PropertyValue): `propertyID` = the identifier *scheme* (e.g. `https://registry.identifiers.org/registry/doi`), `value` = the bare id, `url` = the resolvable form. Alternate identifiers go in `schema:sameAs`, not a second `schema:identifier`.
- **`cdi:LongDataStructure`** requires **exactly one** `IdentifierComponent` (`maxContains: 1`). In the OpenAQ long format, `location_id` is the identifier; `sensors_id`/`datetime` are `AttributeComponent`s (like the DDI-CDI vitals example's timestamp), not identifiers.
- **Instrument nesting**: records use `instrument › sensor › sensingElement` (recursive `schema:hasPart`). The Instrument bblock source (`metadataBuildingBlocks/.../instrument/schema.yaml`) was relaxed to allow this; its generated `resolvedSchema.json`/`instrumentSchema.json` regenerate via the normal bblocks build (the `ogc.na` tooling is not installed in the repo `.venv`).
- **`prov:wasGeneratedBy`** nodes are dual-typed `["prov:Activity","schema:Action"]` because they carry schema.org Action properties (`schema:instrument`, `schema:location`).
- **Vocabulary mappings**: use `skos:exactMatch` only for genuine equivalents (EEA pollutant/method codes), `skos:closeMatch` otherwise (CF standard names), and mint locally with a `skos:editorialNote` where no external term exists (reference-vs-low-cost, static-vs-mobile, electrochemical).
