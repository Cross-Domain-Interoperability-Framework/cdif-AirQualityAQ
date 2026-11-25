# cdif-AirQualityAQ

A working repository for building an **Air-Quality (AQ) profile of the [CDIF](https://cdif.codata.org/) metadata framework** for **low-cost air-quality sensor (LCS) data**. It collects the source metadata schemas that AQ data providers use, crosswalks them to the CDIF profiles, captures what CDIF does not yet cover, and demonstrates the result with validated example metadata records and the controlled vocabularies they need.

CDIF (the Cross-Domain Interoperability Framework) expresses dataset metadata as schema.org + PROV + DQV + DDI-CDI JSON-LD, organised into composable *profiles*. This repo is the air-quality domain application of that framework.

> **Status:** draft / under development. The IRIs under `https://w3id.org/cdif/airquality/…` used in the vocabularies and example records are **placeholders — not yet registered** on w3id.org.

---

## 1. What problem this repo addresses

Low-cost air-quality sensors are reported through several incompatible metadata models (EEA/AAQD reporting templates, OpenAQ, Sensor.community, per-network intake forms, processed research datasets). To make these discoverable and interoperable, their metadata properties need to be mapped onto a common framework (CDIF) and the gaps turned into a small domain extension. This repo does that mapping and proves it out end-to-end.

The companion analysis (how the crosswalk and decisions were derived) lives in `AQ_CDIF_profile_mapping.xlsx`.

---

## 2. Where the contents came from

| Artifact | Source |
|---|---|
| `docs/LCSmetadata__.xlsx` | Original proposed LCS reporting template (author "GSS"), loosely following EEA e-Reporting under the EU Ambient Air Quality Directive (AAQD 2024/2881). The unmodified source. |
| `docs/LCSmetadataAnnotated.xlsx` | Working/annotated copy of the LCS template. The `proposed tables` sheet defines a relational model: Measurement Location → Sampling Point → Sensor Device → Sensing Element → Deployment → Calibration → Measurements. |
| `docs/AirGradient_metadata_annotated.xlsx` | One network's (AirGradient) answers to a data-provider intake questionnaire; row 1 annotates each question with a schema.org-style property label. |
| `FILTER_ReadMe_DataDescriptor.pdf`, `docs/figshare_27195720_metadata.json` | Documentation + Figshare record for the **FILTER** dataset: *Harmonized, Standardized, and Corrected Crowd-Sourced Low-Cost Sensor PM2.5 Data from Sensor.community and PurpleAir Networks Across Europe* (Hassani, Salamalikis, Schneider, Stebel & Castell, NILU; J. Environ. Management 380, 125100, 2025). DOI [10.6084/m9.figshare.27195720](https://doi.org/10.6084/m9.figshare.27195720), CC BY 4.0. |
| `data_examples/` raw CSVs | Harvested samples: per-sensor CSVs from the FILTER Figshare dataset, and per-location daily CSVs from the open [OpenAQ S3 archive](https://openaq-data-archive.s3.amazonaws.com/). |
| `data_examples/*/location-*-metadata.json` | Raw OpenAQ v3 API location records (`api.openaq.org/v3/locations/{id}`), kept as the source metadata the CDIF records are derived from. |

The **CDIF profiles and building blocks** the mapping targets are sibling repositories under `C:\GithubC\CDIF\`: `profile-core`, `profile-discovery`, `profile-datadescription`, `profile-datastructure`, `profile-access`, `profile-codelist`, `profile-conceptscheme`, and the Instrument building block in `metadataBuildingBlocks/_sources/schemaorgProperties/instrument/`.

---

## 3. Repository layout

```
cdif-AirQualityAQ/
├── README.md                          ← this file
├── CLAUDE.md                          ← notes for AI assistants working here
│
│  ── Source metadata schemas + reference material ──
├── docs/
│   ├── LCSmetadata__.xlsx              ← original EEA/AAQD-aligned LCS template
│   ├── LCSmetadataAnnotated.xlsx       ← annotated working copy
│   ├── AirGradient_metadata_annotated.xlsx ← AirGradient intake questionnaire
│   └── figshare_27195720_metadata.json ← FILTER Figshare record
├── FILTER_ReadMe_DataDescriptor.pdf    ← FILTER dataset data descriptor (PDF)
│
│  ── The crosswalk (main analysis deliverable) ──
├── AQ_CDIF_profile_mapping.xlsx
│
│  ── Harvested data + CDIF instance records ──
├── data_examples/
│   ├── SMR_PurpleAir/                 ← FILTER PurpleAir (San Marino), correction empty
│   ├── CHE_corrected/                 ← FILTER PurpleAir (Switzerland), raw + corrected + CI
│   ├── ALB_SensorCommunity/           ← FILTER Sensor.community (Albania)
│   ├── OpenAQ_reference_AirNow_US/    ← US EPA AirNow reference monitor (gases in ppm)
│   ├── OpenAQ_reference_SINCA_Chile/  ← Chile SINCA reference monitor (gases in µg/m³)
│   └── OpenAQ_lowcost_AirGradient_US/ ← AirGradient low-cost sensor
│       └── each folder: <raw>.csv, [location-*-metadata.json], *-cdif.jsonld
│
│  ── Controlled vocabularies (SKOS concept schemes) ──
├── vocabularies/
│   ├── pollutant.jsonld   measurement-method.jsonld   station-class.jsonld
│   └── mobility.jsonld    qc.jsonld                    activity.jsonld
│
│  ── Generators (provenance / reproducibility) ──
└── scripts/
    ├── build_mapping_xlsx.py   build_instances.py   build_vocabularies.py
```

---

## 4. The crosswalk — `AQ_CDIF_profile_mapping.xlsx`

A property-by-property mapping of **234 source metadata properties** (from the LCS template, AirGradient intake, OpenAQ, Sensor.community, and the FILTER sample-data columns) onto the seven CDIF profiles.

- **`Mapping`** sheet — `Variable · Variable source · Source group · Obligation · EEA/EU equivalent · CDIF property (target) · CDIF profile · Match status · Mapping note · Example value`. Status is `mapped` / `partial` / `excluded` (≈216 / 13 / 5 after review).
- **`Gaps (extension schema)`** sheet — source properties with no CDIF match.
- **`Extension concepts`** sheet — the gaps consolidated into themes.

Key modelling decisions captured in the mapping and realised in the examples:

- Devices map onto the **Instrument building block** via `prov:wasGeneratedBy.schema:instrument` (manufacturer / model / identifier / validFrom-Through / additionalProperty / hasPart).
- Sensor **siting context** (building/kerb/emission-source distances, inlet height) → `prov:wasGeneratedBy.schema:location.schema:Place.schema:additionalProperty`, distinct from `schema:spatialCoverage` (the measurement location).
- Classifications (`isMonitor`, `isMobile`, deployment type, sensor type) → `schema:additionalType` with controlled vocabularies.
- QC flags, siting metrics, etc. → `schema:additionalProperty` soft-typed `PropertyValue`s with controlled `propertyID`s.
- No new "hard" schema types are required — the remaining work is **vocabularies** (see §6).

---

## 5. Example metadata records — `data_examples/`

Each folder holds the **raw data CSV**, the **source metadata** it was derived from, and a **CDIF JSON-LD instance** (`*-cdif.jsonld`). The six records exercise the whole profile stack and two physical data shapes:

| Folder | Record | Physical shape | CDIF profiles it conforms to |
|---|---|---|---|
| `SMR_PurpleAir` | PA179671 | wide CSV | core + discovery + **datadescription** |
| `CHE_corrected` | PA112746 | wide CSV (raw + corrected + CI) | core + discovery + **datadescription** |
| `ALB_SensorCommunity` | SC8323 | wide CSV | core + discovery + **datadescription** |
| `OpenAQ_reference_AirNow_US` | 2178 | long / EAV CSV | core + discovery + **datastructure** |
| `OpenAQ_reference_SINCA_Chile` | 844 | long / EAV CSV | core + discovery + **datastructure** |
| `OpenAQ_lowcost_AirGradient_US` | 1236012 | long / EAV CSV | core + discovery + **datastructure** |

All six also use the **Instrument** building block (nested `instrument › sensor › sensingElement`) and the **access** profile (ODRL license terms).

- **FILTER (wide)** records model each CSV column as a `cdi:InstanceVariable` (`cdif:role`/`physicalDataType`); the confidence-interval columns `cdif:qualifies` the corrected-PM2.5 variable; the distribution carries a `cdif:hasPhysicalMapping`.
- **OpenAQ (long/EAV)** records attach a `cdi:LongDataStructure` to the distribution (`cdi:isStructuredBy`): one `IdentifierComponent`, a `VariableDescriptorComponent` (the `parameter` column mapping each pollutant token to its variable), a `VariableValueComponent` (the `value` column), and `AttributeComponent`s (`sensors_id`/`datetime`/`units`/`lat`/`lon`). Note the DDI-CDI constraint: a `LongDataStructure` allows **exactly one** `IdentifierComponent`, so time/sensor keys are Attributes.

`location-1236012-metadata.json` (raw OpenAQ) vs `location-1236012-cdif.jsonld` (CDIF) is a clear before/after of the crosswalk.

---

## 6. Vocabularies — `vocabularies/`

Six CDIF `skos:ConceptScheme` documents (conforming to the `conceptscheme` profile) providing the controlled terms the `additionalType` / `additionalProperty` / `propertyID` slots reference. Where an established term exists it is linked with `skos:exactMatch` / `skos:closeMatch`; where none exists the concept is minted locally with a `skos:editorialNote`.

| Scheme | Concepts | External mappings |
|---|---|---|
| `pollutant.jsonld` | 8 | `exactMatch` → EEA/Eionet `aq/pollutant`; `closeMatch` → CF standard names (NERC NVS) |
| `measurement-method.jsonld` | 10 | `exactMatch` → EEA `aq/measurementmethod` (NDIR, UV-P, UV-FL, chemi, BETA, GRAVIMETRIC); OPC → `closeMatch` OPC-CMC |
| `station-class.jsonld` | 2 | *local* — reference-monitor / low-cost-sensor (no established term; see CEN/TS 17660, WMO GAW) |
| `mobility.jsonld` | 2 | *local* — static / mobile (EEA carries only a boolean; SOSA only `sosa:Platform`) |
| `qc.jsonld` | 9 | *local* — the FILTER 5-step QC + correction + validity/verification |
| `activity.jsonld` | 4 | *local* — observation / data-reduction / calibration / deployment |

Measurement-category / site-area fields reuse EEA `aq/stationclassification` and `aq/areaclassification` directly (no local scheme needed).

---

## 7. Generators — `scripts/`

The crosswalk workbook, the instance records, and the vocabularies are machine-generated; these scripts are kept for provenance and reproducibility.

| Script | Produces |
|---|---|
| `build_mapping_xlsx.py` | `AQ_CDIF_profile_mapping.xlsx` |
| `build_instances.py` | the six `data_examples/*/*-cdif.jsonld` records (and patches the hand-authored AirGradient one) |
| `build_vocabularies.py` | the six `vocabularies/*.jsonld` concept schemes |

> These are the **as-run** generators. They contain **absolute paths** to the sibling CDIF profile repositories under `C:\GithubC\CDIF\` (used to validate output against each profile's `*StructuredSchema.json`) and to the harvested source files. Adjust those paths to re-run elsewhere. They require Python with `openpyxl` and `jsonschema`.

---

## 8. Validating the outputs

Every instance record and vocabulary validates against the relevant CDIF profile JSON Schema with **0 errors**. To re-validate, point `jsonschema` at the profile `*StructuredSchema.json`:

```python
import json, jsonschema
schema = json.load(open(r"C:\GithubC\CDIF\profile-discovery\cdifDiscoveryStructuredSchema.json", encoding="utf-8"))
doc    = json.load(open(r"data_examples\CHE_corrected\PA112746-cdif.jsonld", encoding="utf-8"))
errs   = list(jsonschema.Draft202012Validator(schema).iter_errors(doc))
print(len(errs), "errors")
```

Profiles used: `cdifDiscoveryStructuredSchema.json` (all records), `cdifDataDescriptionStructuredSchema.json` (FILTER records), `cdifDataStructureStructuredSchema.json` (OpenAQ records), `cdifConceptSchemeStructuredSchema.json` (vocabularies).

---

## 9. Related upstream change

As part of this work the shared **Instrument building block** was relaxed to allow recursive `schema:hasPart`, so `instrument › sensor › sensingElement` hierarchies are first-class. The source change is in `metadataBuildingBlocks/_sources/schemaorgProperties/instrument/schema.yaml` (the generated `resolvedSchema.json` / `instrumentSchema.json` regenerate via the normal bblocks build).

---

## 10. Data licensing

The harvested data samples retain their source licenses: the FILTER samples are **CC BY 4.0**; OpenAQ AirNow is **US Public Domain**, AirGradient is **CC BY 4.0**, and Chile/SINCA has no license stated by the provider. Consult each source before reuse. Licensing of the derived CDIF artifacts in this repo is to be decided by the maintainer.

---

## Maintainer

Stephen Richard — <smrTucson@gmail.com> — GitHub [@smrgeoinfo](https://github.com/smrgeoinfo)
