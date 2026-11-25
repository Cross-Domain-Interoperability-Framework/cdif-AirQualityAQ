# Generate CDIF conceptscheme JSON-LD vocabularies for the AQ profile; validate each.
# Native concept definitions here; external skos-match URIs filled into MATCHES (verified, not guessed).
import json, os
try:
    import jsonschema
    SCHEMA=json.load(open(r"C:/GithubC/CDIF/profile-conceptscheme/cdifConceptSchemeStructuredSchema.json",encoding="utf-8"))
except Exception as e:
    SCHEMA=None; print("schema load issue:",e)

OUT=r"C:/GithubC/CDIF/cdif-AirQualityAQ/vocabularies"
os.makedirs(OUT, exist_ok=True)
BASE="https://w3id.org/cdif/airquality/vocab/"
CTX={"skos":"http://www.w3.org/2004/02/skos/core#","schema":"http://schema.org/","dcterms":"http://purl.org/dc/terms/","dcat":"http://www.w3.org/ns/dcat#"}

# ---- external vocabulary bases (verified) ----
EEA_POL="http://dd.eionet.europa.eu/vocabulary/aq/pollutant/"
EEA_MM="http://dd.eionet.europa.eu/vocabulary/aq/measurementmethod/"
EEA_AT="http://dd.eionet.europa.eu/vocabulary/aq/analyticaltechnique/"
CF="http://vocab.nerc.ac.uk/standard_name/"

# ---- MATCHES: "scheme/local-id" -> list of (predicate, uri) ----  VERIFIED URIs only.
MATCHES = {
 # measurement methods -> EEA Eionet AQD measurementmethod / analyticaltechnique
 "measurement-method/NDIR":[("skos:exactMatch",EEA_MM+"NDIR")],
 "measurement-method/UV-photometry":[("skos:exactMatch",EEA_MM+"UV-P")],
 "measurement-method/UV-fluorescence":[("skos:exactMatch",EEA_MM+"UV-FL")],
 "measurement-method/chemiluminescence":[("skos:exactMatch",EEA_MM+"chemi"),("skos:closeMatch",EEA_AT+"CHEMI")],
 "measurement-method/beta-attenuation":[("skos:exactMatch",EEA_MM+"BETA")],
 "measurement-method/gravimetry":[("skos:exactMatch",EEA_MM+"GRAVIMETRIC"),("skos:closeMatch",EEA_AT+"gravi")],
 "measurement-method/OPC":[("skos:closeMatch",EEA_MM+"OPC-CMC")],
 # pollutants -> EEA pollutant (substance, AQD canonical) exactMatch + CF standard name (observable) closeMatch
 "pollutant/PM2.5":[("skos:exactMatch",EEA_POL+"6001"),("skos:closeMatch",CF+"mass_concentration_of_pm2p5_ambient_aerosol_particles_in_air/")],
 "pollutant/PM10":[("skos:exactMatch",EEA_POL+"5"),("skos:closeMatch",CF+"mass_concentration_of_pm10_ambient_aerosol_particles_in_air/")],
 "pollutant/O3":[("skos:exactMatch",EEA_POL+"7"),("skos:closeMatch",CF+"mole_fraction_of_ozone_in_air/")],
 "pollutant/NO2":[("skos:exactMatch",EEA_POL+"8"),("skos:closeMatch",CF+"mole_fraction_of_nitrogen_dioxide_in_air/")],
 "pollutant/SO2":[("skos:exactMatch",EEA_POL+"1"),("skos:closeMatch",CF+"mole_fraction_of_sulfur_dioxide_in_air/")],
 "pollutant/CO":[("skos:exactMatch",EEA_POL+"10"),("skos:closeMatch",CF+"mole_fraction_of_carbon_monoxide_in_air/")],
 "pollutant/NO":[("skos:exactMatch",EEA_POL+"38")],
 "pollutant/NOx":[("skos:exactMatch",EEA_POL+"9")],
}
# editorial notes for concepts with a gap or a candidate mapping to verify
EDNOTE = {
 "measurement-method/OPC":"closeMatch to EEA measurementmethod/OPC-CMC (optical particle counter + conversion to mass); a bare 'optical particle counter' EEA term was not confirmed, and light-scattering/nephelometry notations exist but are unconfirmed.",
 "measurement-method/EC":"No EEA reference-method term for electrochemical (amperometric) gas sensing; electrochemistry is primarily a low-cost-sensor technique. Local concept retained (gap in EEA vocab).",
 "measurement-method/CAP":"Capacitive relative-humidity sensing; no EEA air-pollutant method term (RH is a covariate, not a regulated pollutant).",
 "measurement-method/RTD":"Resistance temperature detector; no EEA air-pollutant method term (temperature is a covariate).",
 "station-class/reference-monitor":"No established resolvable SKOS term for reference-grade vs low-cost; local concept minted. See CEN/TS 17660 and WMO/GAW guidance. NB EEA aq/stationclassification (background/industrial/traffic) is a different axis (site type, not instrument grade).",
 "station-class/low-cost-sensor":"No established resolvable SKOS term; local concept minted. See CEN/TS 17660 (performance evaluation of air-quality sensor systems).",
 "mobility/static":"No established SKOS term; EEA AQD encodes mobility as a boolean field and SOSA has sosa:Platform but no fixed/mobile concept. Local concept minted.",
 "mobility/mobile":"No established SKOS term; local concept minted (see mobility/static).",
 "qc/validity":"Candidate mapping to the EEA e-Reporting observation-validity flag vocabulary under dd.eionet.europa.eu/vocabulary/aq/ (verify exact scheme/term URIs).",
 "qc/verification":"Candidate mapping to the EEA e-Reporting verification flag vocabulary (verify exact scheme/term URIs).",
 "pollutant/PM2.5":"exactMatch is to the EEA AQD pollutant term (the AQ-domain canonical identifier for the measured pollutant); the CF standard name is closeMatch because it denotes the observable quantity and units (mass concentration in air) rather than the substance. Same pattern applies to the other pollutant concepts.",
}

def concept(scheme, lid, pref, defn, notation=None, alt=None, note=None, broader=None):
    c={"@id":BASE+scheme+"/"+lid,"@type":["skos:Concept"],
       "skos:prefLabel":pref,"skos:definition":defn,
       "skos:inScheme":{"@id":BASE+scheme}}
    if notation: c["skos:notation"]=notation
    if alt: c["skos:altLabel"]=alt
    if note: c["skos:note"]=note
    if broader: c["skos:broader"]=[{"@id":BASE+scheme+"/"+b} for b in broader]
    for pred,uri in MATCHES.get(scheme+"/"+lid, []):
        c.setdefault(pred,[]).append({"@id":uri})
    if scheme+"/"+lid in EDNOTE:
        c["skos:editorialNote"]=EDNOTE[scheme+"/"+lid]
    # collapse single-item match arrays is optional; keep arrays (valid)
    return c

def scheme_doc(scheme, title, defn, concepts, version="0.1.0"):
    return {"@context":CTX,"@id":BASE+scheme,"@type":["skos:ConceptScheme"],
      "skos:prefLabel":title,"skos:definition":defn,"schema:version":version,
      "skos:hasTopConcept":concepts,
      "schema:subjectOf":{"@id":BASE+scheme+"/record","@type":["schema:Dataset"],
        "schema:additionalType":[{"@id":"dcat:CatalogRecord"}],
        "schema:about":{"@id":BASE+scheme},
        "dcterms:conformsTo":[{"@id":"https://w3id.org/cdif/conceptscheme/2.0"}]}}

SCHEMES={}

# 1. station-class
SCHEMES["station-class"]=scheme_doc("station-class",
 "AQ station / instrument class",
 "Classification of air-quality measurement platforms by grade: reference/regulatory-grade monitors vs low-cost sensors. Used on schema:additionalType of the instrument. Maps OpenAQ isMonitor and OpenAQ instrument 'Government Monitor'.",
 [concept("station-class","reference-monitor","Reference-grade monitor",
    "A regulatory / reference-grade air-quality monitoring instrument operated to a recognized reference or equivalent method (e.g. an EU AAQD reference method, or a US EPA Federal Reference/Equivalent Method). Corresponds to OpenAQ isMonitor = true.",
    "reference-monitor", alt=["reference monitor","regulatory monitor"]),
  concept("station-class","low-cost-sensor","Low-cost air-quality sensor",
    "A low-cost air-quality sensor device, typically community- or citizen-operated and not of reference grade; requires correction/QC for regulatory-comparable use. Corresponds to OpenAQ isMonitor = false.",
    "low-cost-sensor", alt=["LCS","low-cost sensor"])])

# 2. mobility
SCHEMES["mobility"]=scheme_doc("mobility",
 "Measurement platform mobility",
 "Whether a measurement platform is stationary or mobile. Used on schema:additionalType of the deployment activity (prov:wasGeneratedBy.schema:Action). Maps OpenAQ isMobile and the LCS 'Monitoring mode'.",
 [concept("mobility","static","Stationary","A fixed-location measurement platform whose position does not change during the monitoring period. Corresponds to OpenAQ isMobile = false.","static",alt=["fixed","stationary"]),
  concept("mobility","mobile","Mobile","A measurement platform whose geographic location varies over time; per-observation coordinates are provided. Corresponds to OpenAQ isMobile = true.","mobile")])

# 3. measurement-method (sensing principle)
SCHEMES["measurement-method"]=scheme_doc("measurement-method",
 "AQ measurement method / sensing principle",
 "Sensing principle / analytical technique used by a sensing element or reference analyser. Low-cost codes (OPC/EC/NDIR/CAP/RTD) follow the LCS reporting template; reference methods cover regulatory analysers. Maps to the EEA/Eionet AQ analytical-technique / measurement-method vocabularies.",
 [concept("measurement-method","OPC","Optical particle counting","Optical particle counting by laser light scattering; the common low-cost particulate-matter sensing principle.","OPC",alt=["optical particle counter","laser light scattering"]),
  concept("measurement-method","EC","Electrochemical sensing","Electrochemical (amperometric) gas sensing, common in low-cost NO2 / O3 / CO sensors.","EC",alt=["electrochemical","amperometric"]),
  concept("measurement-method","NDIR","Non-dispersive infrared","Non-dispersive infrared absorption; common for CO2 and CO.","NDIR"),
  concept("measurement-method","CAP","Capacitive sensing","Capacitive sensing, typically for relative humidity.","CAP",alt=["capacitive"]),
  concept("measurement-method","RTD","Resistance temperature detector","Resistance temperature detector; temperature sensing.","RTD"),
  concept("measurement-method","beta-attenuation","Beta-ray attenuation","Beta-ray attenuation monitoring; a reference/equivalent method for particulate mass.","beta-attenuation",alt=["BAM","beta attenuation"]),
  concept("measurement-method","gravimetry","Gravimetry","Gravimetric determination of particulate mass on a filter; PM reference method.","gravimetry"),
  concept("measurement-method","UV-photometry","UV photometry","Ultraviolet photometric absorption; ozone reference method.","UV-photometry"),
  concept("measurement-method","UV-fluorescence","UV fluorescence","Ultraviolet fluorescence; sulphur dioxide reference method.","UV-fluorescence"),
  concept("measurement-method","chemiluminescence","Chemiluminescence","Chemiluminescence; nitrogen oxides (NO/NO2/NOx) reference method.","chemiluminescence")])

# 4. qc (FILTER QC steps + correction)
SCHEMES["qc"]=scheme_doc("qc",
 "AQ quality-control steps and flags",
 "Quality-control checks and correction diagnostics applied to low-cost sensor data. The first five correspond to the positions of the FILTER 5-character QC flag string (raw_qc / corrected_qc). Used as dqv:isMeasurementOf.",
 [concept("qc","range-validity","Range validity","QC step: whether a value is within the plausible physical range (0–1000 µg/m³ for PM2.5). FILTER flag position 1 (0 out of range, 1 within range).","range-validity"),
  concept("qc","constant-value","Constant-value check","QC step: detects a sensor reporting near-constant (stuck) values over a moving window. FILTER flag position 2 (0 insufficient data, 1 stuck, 2 varying).","constant-value"),
  concept("qc","outlier","Outlier detection","QC step: detects outliers using median absolute deviation and neighbour cross-checks. FILTER flag position 3 (0 no data, 1 self-outlier, 2 neighbour-confirmed, 3 not outlier).","outlier"),
  concept("qc","spatial-correlation","Spatial correlation","QC step: tests Pearson correlation of the sensor with neighbours over a rolling window. FILTER flag position 4 (3 = correlated with neighbours).","spatial-correlation"),
  concept("qc","spatial-similarity","Spatial similarity","QC step: tests similarity of the sensor to nearby reference stations. FILTER flag position 5 (3 = similar to reference).","spatial-similarity"),
  concept("qc","correction-improvement","Correction improvement","Diagnostic: whether the distant-correction model reduced the normalized RMSE versus reference for an observation (0/1).","correction-improvement"),
  concept("qc","correction-method","Correction method applied","The correction / bias-adjustment algorithm applied to raw sensor values (e.g. EPA correction, distant LCS correction).","correction-method"),
  concept("qc","validity","Validity","Whether a measurement value is valid (valid / not valid / below detection). Aligns with EEA e-Reporting validity flags.","validity"),
  concept("qc","verification","Verification","Whether quality control / verification has been performed on a value. Aligns with EEA e-Reporting verification flags.","verification")])

# 5. activity (provenance activity types)
SCHEMES["activity"]=scheme_doc("activity",
 "AQ provenance activity types",
 "Types of prov:Activity in the air-quality data lifecycle, used on schema:additionalType of a prov:Activity (prov:wasGeneratedBy).",
 [concept("activity","observation","Observation","The in-situ measurement/observation activity that produced the raw values.","observation"),
  concept("activity","data-reduction","Data reduction / correction","Processing that harmonizes, quality-controls and corrects raw sensor data into analysis-ready values (e.g. the FILTER framework).","data-reduction",alt=["correction","processing"]),
  concept("activity","calibration","Calibration","A calibration process relating sensor response to a reference (lab / field / co-location / model).","calibration"),
  concept("activity","deployment","Deployment","Deployment of a sensor or instrument to a site for a monitoring period.","deployment")])

# 6. pollutant / observed air-quality variable (carries the EEA<->CF crosswalk)
SCHEMES["pollutant"]=scheme_doc("pollutant",
 "AQ pollutants / measured variables",
 "Air-quality pollutants and co-measured variables used as schema:propertyID / schema:variableMeasured. Each concept carries skos:exactMatch to the EEA/Eionet AQD pollutant term (AQD canonical identifier) and skos:closeMatch to the corresponding CF standard name (observable quantity). Use these in place of bare term-code strings.",
 [concept("pollutant","PM2.5","Particulate matter < 2.5 µm","Mass concentration of particulate matter with aerodynamic diameter < 2.5 µm in ambient air.","PM2.5",alt=["PM2.5"]),
  concept("pollutant","PM10","Particulate matter < 10 µm","Mass concentration of particulate matter with aerodynamic diameter < 10 µm in ambient air.","PM10"),
  concept("pollutant","O3","Ozone","Ozone in ambient air.","O3",alt=["ozone"]),
  concept("pollutant","NO2","Nitrogen dioxide","Nitrogen dioxide in ambient air.","NO2"),
  concept("pollutant","SO2","Sulphur dioxide","Sulphur dioxide in ambient air.","SO2",alt=["sulfur dioxide"]),
  concept("pollutant","CO","Carbon monoxide","Carbon monoxide in ambient air.","CO"),
  concept("pollutant","NO","Nitrogen monoxide","Nitrogen monoxide (nitric oxide) in ambient air.","NO",alt=["nitric oxide"]),
  concept("pollutant","NOx","Nitrogen oxides","Nitrogen oxides in ambient air, reported as NO2 equivalent.","NOX as NO2",alt=["NOx","NOX"])])

# ---- write + validate ----
results=[]
for scheme,doc in SCHEMES.items():
    path=os.path.join(OUT, scheme+".jsonld")
    with open(path,"w",encoding="utf-8") as fh: json.dump(doc,fh,indent=2,ensure_ascii=False)
    st="written"
    if SCHEMA is not None:
        v=jsonschema.Draft202012Validator(SCHEMA)
        errs=sorted(v.iter_errors(doc), key=lambda e:list(e.path))
        st=f"{len(errs)} error(s)"
        for e in errs[:6]: print("  ERR",scheme,list(e.path)[:5],"->",e.message[:110])
    nmatch=sum(1 for c in doc["skos:hasTopConcept"] for k in c if k.startswith("skos:") and "Match" in k)
    results.append((scheme,len(doc["skos:hasTopConcept"]),nmatch,st))
for r in results: print(f"{r[0]:20} concepts={r[1]} match-props={r[2]} | {r[3]}")
print("done — MATCHES entries:",sum(len(v) for v in MATCHES.values()))
