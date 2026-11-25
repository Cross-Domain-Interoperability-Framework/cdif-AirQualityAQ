# Generate CDIF instance documents for the remaining 5 data_examples; validate each against the discovery profile.
import json, os
try:
    import jsonschema
    SCHEMA=json.load(open(r"C:/GithubC/CDIF/profile-discovery/cdifDiscoveryStructuredSchema.json",encoding="utf-8"))
except Exception as e:
    SCHEMA=None; print("jsonschema/schema load issue:",e)

BASE=r"C:/GithubC/CDIF/cdif-AirQualityAQ/data_examples"
CTX={"schema":"http://schema.org/","aq":"https://w3id.org/cdif/airquality/examples/","dcterms":"http://purl.org/dc/terms/","dcat":"http://www.w3.org/ns/dcat#","prov":"http://www.w3.org/ns/prov#","spdx":"http://spdx.org/rdf/terms#","dqv":"http://www.w3.org/ns/dqv#","geosparql":"http://www.opengis.net/ont/geosparql#","sf":"http://www.opengis.net/ont/sf#","time":"http://www.w3.org/2006/time#","cdi":"http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/","cdif":"https://w3id.org/cdif/","skos":"http://www.w3.org/2004/02/skos/core#"}
MM="https://w3id.org/cdif/airquality/vocab/measurement-method"
EEA="http://dd.eionet.europa.eu/vocabulary/aq/pollutant"
QUDT={"ug":"http://qudt.org/vocab/unit/MicroGM-PER-M3","ppm":"http://qudt.org/vocab/unit/PPM","C":"http://qudt.org/vocab/unit/DEG_C","pct":"http://qudt.org/vocab/unit/PERCENT"}
STATION="https://w3id.org/cdif/airquality/vocab/station-class"
MOBILITY="https://w3id.org/cdif/airquality/vocab/mobility"
QCVOC="https://w3id.org/cdif/airquality/vocab/qc"
CCBY={"@id":"https://creativecommons.org/licenses/by/4.0/","@type":["schema:CreativeWork"],"schema:name":"Creative Commons Attribution 4.0 International (CC BY 4.0)","schema:url":"https://creativecommons.org/licenses/by/4.0/"}

def dterm(name, scheme=None, code=None):
    d={"@type":["schema:DefinedTerm"],"schema:name":name}
    if scheme: d["schema:inDefinedTermSet"]=scheme
    if code: d["schema:termCode"]=code
    # link to the concept @id when referencing an AQ-profile vocabulary scheme
    if scheme and code and scheme.startswith("https://w3id.org/cdif/airquality/vocab/"):
        d["schema:identifier"]=scheme+"/"+code
    return d

POLMAP={"NOX":"NOx"}
def pollutant(label):
    lid=POLMAP.get(label,label)
    return [{"@id":"https://w3id.org/cdif/airquality/vocab/pollutant/"+lid}]

def var(vid,name,unit_text,unit_key=None,propID=None,alt=None,desc=None):
    v={"@id":"aq:"+vid,"@type":["schema:PropertyValue"],"schema:name":name}
    if desc: v["schema:description"]=desc
    if alt: v["schema:alternateName"]=[alt]
    v["schema:propertyID"]=propID if propID is not None else [name]
    if unit_text: v["schema:unitText"]=unit_text
    if unit_key: v["schema:unitCode"]={"@id":QUDT[unit_key]}
    return v

def qc_measure(step_name, code, meaning):
    return {"@type":["dqv:QualityMeasurement"],
            "dqv:isMeasurementOf":dterm(step_name, QCVOC, code),
            "dqv:value":meaning}

FILTER_QC=[
 qc_measure("Range validity","range","per-hour flag (pos.1 of raw_qc/corrected_qc): 0 out of range, 1 within range"),
 qc_measure("Constant value","constant","pos.2: 0 insufficient data, 1 stuck, 2 varying"),
 qc_measure("Outlier","outlier","pos.3: 0 no data, 1 self-outlier, 2 neighbour-confirmed outlier, 3 not outlier"),
 qc_measure("Spatial correlation","spatial-correlation","pos.4: 0/1 insufficient, 2 fails r~0.7, 3 correlated with neighbours"),
 qc_measure("Spatial similarity","spatial-similarity","pos.5: 0/1 insufficient, 2 fails, 3 similar to reference"),
]

def build(cfg):
    inst={"@context":CTX,"@id":cfg["id"],"@type":["schema:Dataset"],
          "schema:name":cfg["name"],"schema:description":cfg["desc"],
          "schema:identifier":cfg["identifier"],
          "schema:additionalType":[dterm(cfg["classname"],STATION,cfg["classcode"])],
          "schema:dateModified":cfg["modified"],
          "schema:url":cfg.get("url")}
    if cfg.get("sameAs"): inst["schema:sameAs"]=cfg["sameAs"]
    if cfg.get("measurementTechnique"): inst["schema:measurementTechnique"]=cfg["measurementTechnique"]
    if cfg.get("license"): inst["schema:license"]=cfg["license"]
    if cfg.get("conditionsOfAccess"): inst["schema:conditionsOfAccess"]=cfg["conditionsOfAccess"]
    inst["schema:keywords"]=cfg.get("keywords",["air quality","particulate matter"])
    if cfg.get("creator"): inst["schema:creator"]={"@list":cfg["creator"]}
    if cfg.get("contributor"): inst["schema:contributor"]=cfg["contributor"]
    if cfg.get("publisher"): inst["schema:publisher"]=cfg["publisher"]
    if cfg.get("provider"): inst["schema:provider"]=cfg["provider"]
    inst["schema:distribution"]=cfg["distribution"]
    if cfg.get("long"):
        pv={v["schema:name"]:v["@id"] for v in cfg["variables"]}
        inst["schema:distribution"][0]["@type"]=["schema:DataDownload","cdi:TabularTextDataSet","cdi:PhysicalDataSet"]
        inst["schema:distribution"][0]["cdi:isStructuredBy"]=long_structure(cfg["id"],pv)
    if cfg.get("relatedLink"): inst["schema:relatedLink"]=cfg["relatedLink"]
    inst["schema:variableMeasured"]=cfg["variables"]
    inst["schema:spatialCoverage"]=cfg["spatial"]
    inst["schema:temporalCoverage"]=[cfg["temporal"]]
    if cfg.get("dqv"): inst["dqv:hasQualityMeasurement"]=cfg["dqv"]
    inst["prov:wasGeneratedBy"]=cfg["wasGeneratedBy"]
    if cfg.get("wasDerivedFrom"): inst["prov:wasDerivedFrom"]=cfg["wasDerivedFrom"]
    inst["schema:subjectOf"]={"@id":cfg["id"]+"-record","@type":["schema:Dataset"],
        "schema:additionalType":[{"@id":"dcat:CatalogRecord"}],
        "schema:about":{"@id":cfg["id"]},
        "dcterms:conformsTo":[{"@id":"https://w3id.org/cdif/core/2.0"},{"@id":"https://w3id.org/cdif/discovery/2.0"}]+[{"@id":u} for u in cfg.get("conformsExtra",[])],
        "schema:dateModified":cfg["modified"],
        "schema:maintainer":{"@type":["schema:Organization"],"schema:name":"CDIF Air-Quality profile (example instance)"},
        "schema:includedInDataCatalog":cfg["catalog"]}
    return inst

# ---- shared actors ----
NILU={"@type":["schema:Organization"],"schema:name":"NILU","schema:url":"https://nilu.com"}
FILTER_CREATORS=[{"@type":["schema:Person"],"schema:name":n,"schema:affiliation":{"@id":"https://nilu.com"}} for n in
  ["Hassani, Amirhossein","Salamalikis, Vasileios","Schneider, Philipp","Stebel, Kerstin","Castell, Núria"]]
FIGSHARE={"@type":["schema:DataDownload"],"schema:name":"FILTER dataset (per-country ZIP, Figshare)","schema:contentUrl":"https://doi.org/10.6084/m9.figshare.27195720","schema:encodingFormat":["text/csv","application/zip"]}
def filter_derived(network, url):
    return [{"@id":"aq:raw-"+network.lower().replace('.','').replace(' ',''),"@type":["schema:Dataset"],"schema:name":"Raw "+network+" low-cost sensor observations","schema:url":url}]
def filter_activity(instrument):
    return [{"@type":["prov:Activity","schema:Action"],
             "schema:additionalType":[dterm("Data reduction / correction (FILTER framework)", "https://w3id.org/cdif/airquality/vocab/activity","data-reduction")],
             "schema:name":"FILTER — Framework for Improving Low-cost Technology Effectiveness and Reliability",
             "schema:instrument":instrument}]
# --- instrument nesting: instrument > sensor > sensingElement (hasPart extension) ---
def sensing_element(name, method_code, method_name):
    return {"@type":["schema:Product"],"schema:name":name,
            "schema:additionalType":[dterm(method_name,MM,method_code)]}
def sensor(name, elements, model=None):
    s={"@type":["schema:Product"],"schema:name":name,"schema:hasPart":elements}
    if model: s["schema:model"]={"@type":["schema:ProductModel"],"schema:name":model}
    return s
def openair(name, manuf, model, sensors=None):
    instr={"@id":"aq:instr-"+name.lower().replace(' ','-'),"@type":["schema:Product"],"schema:name":name,
      "schema:additionalType":[dterm("Low-cost air-quality sensor",STATION,"low-cost-sensor")],
      "schema:manufacturer":{"@type":["schema:Organization"],"schema:name":manuf},
      "schema:hasPart":sensors or []}
    if model: instr["schema:model"]={"@type":["schema:ProductModel"],"schema:name":model}
    return instr
def gov_monitor(analysers=None):
    g={"@id":"aq:instr-gov-monitor","@type":["schema:Product"],"schema:name":"Government reference monitor",
      "schema:additionalType":[dterm("Reference-grade monitor",STATION,"reference-monitor")]}
    if analysers: g["schema:hasPart"]=analysers
    return g

# --- datadescription: InstanceVariables + physical mapping (FILTER wide CSV) ---
def ivar(base, lid, name, role, pdt, unit_text=None, unit_key=None, propID=None, desc=None, qualifies=None):
    v={"@id":base+"/var/"+lid,"@type":["schema:PropertyValue","cdi:InstanceVariable"],
       "schema:name":name,"cdif:name":[name],"cdif:physicalDataType":pdt,"cdif:role":role}
    if desc: v["schema:description"]=desc
    if propID is not None: v["schema:propertyID"]=propID
    if unit_text: v["schema:unitText"]=unit_text
    if unit_key: v["schema:unitCode"]={"@id":QUDT[unit_key]}
    if qualifies: v["cdif:qualifies"]={"@id":base+"/var/"+qualifies}
    return v
def filter_vars(base):
    return [
     ivar(base,"hour_timestamp","hour_timestamp","Dimension","xsd:integer",desc="Hour start, Unix epoch seconds (UTC)"),
     ivar(base,"sensor_id","sensor_id","Descriptor","xsd:string",desc="Sensor/channel identifier (e.g. PurpleAir channel A/B)"),
     ivar(base,"location","location","Descriptor","xsd:string",desc="Sensor location id"),
     ivar(base,"raw_pm2_5","raw_pm2_5","Measure","xsd:decimal","µg/m³","ug",pollutant("PM2.5"),"Raw low-cost PM2.5"),
     ivar(base,"spread","spread","Attribute","xsd:integer",desc="Hour representativeness 1/2/3",qualifies="raw_pm2_5"),
     ivar(base,"raw_qc","raw_qc","Attribute","xsd:string",desc="FILTER 5-step QC flag string",qualifies="raw_pm2_5"),
     ivar(base,"corrected_pm2_5","corrected_pm2_5","Measure","xsd:decimal","µg/m³","ug",pollutant("PM2.5"),"Bias-corrected PM2.5"),
     ivar(base,"corrected_ci_down","corrected_ci_down","Attribute","xsd:decimal","µg/m³","ug",None,"Lower bound of the 95% confidence interval","corrected_pm2_5"),
     ivar(base,"corrected_ci_up","corrected_ci_up","Attribute","xsd:decimal","µg/m³","ug",None,"Upper bound of the 95% confidence interval","corrected_pm2_5"),
     ivar(base,"correction_improvement","correction_improvement","Attribute","xsd:integer",desc="nRMSE-reduction flag 0/1",qualifies="corrected_pm2_5"),
     ivar(base,"corrected_qc","corrected_qc","Attribute","xsd:string",desc="FILTER 5-step QC flag string (corrected)",qualifies="corrected_pm2_5"),
    ]
def filter_csv_dist(folder, fname, desc, base):
    cols=["hour_timestamp","sensor_id","location","raw_pm2_5","spread","raw_qc","corrected_pm2_5","corrected_ci_down","corrected_ci_up","correction_improvement","corrected_qc"]
    pdt={"hour_timestamp":"Integer","sensor_id":"String","location":"String","raw_pm2_5":"Numeric","spread":"Integer","raw_qc":"String","corrected_pm2_5":"Numeric","corrected_ci_down":"Numeric","corrected_ci_up":"Numeric","correction_improvement":"Integer","corrected_qc":"String"}
    mapping=[{"cdif:index":i,"cdif:physicalDataType":pdt[c],"cdi:isRequired":c in ("hour_timestamp","sensor_id","location","raw_pm2_5"),
              "cdif:formats_InstanceVariable":{"@id":base+"/var/"+c}} for i,c in enumerate(cols)]
    return {"@type":["schema:DataDownload","cdi:TabularTextDataSet","cdi:PhysicalDataSet"],
            "schema:name":fname,"schema:description":desc,
            "schema:contentUrl":"https://w3id.org/cdif/airquality/examples/"+folder+"/"+fname,
            "schema:encodingFormat":["text/csv"],
            "cdi:characterSet":"UTF-8","cdi:isDelimited":True,"cdi:delimiter":",","cdi:hasHeader":True,
            "cdi:headerRowCount":1,"cdi:skipRows":0,"cdi:nullSequence":"",
            "cdif:hasPhysicalMapping":mapping}
def tz_location(place, tz):
    return {"@type":["schema:Place"],"schema:name":place,
      "schema:additionalProperty":[{"@type":["schema:PropertyValue"],"schema:name":"time zone","schema:propertyID":["https://www.iana.org/time-zones"],"schema:value":tz}]}
def action(mobility_code, mobility_name, instrument, loc_place, tz):
    return [{"@type":["prov:Activity","schema:Action"],
      "schema:additionalType":[dterm(mobility_name,MOBILITY,mobility_code)],
      "schema:instrument":instrument,
      "schema:location":tz_location(loc_place,tz)}]
def openaq_dist(locid, y, m, d):
    return [
     {"@type":["schema:DataDownload"],"schema:name":f"OpenAQ daily CSV (location {locid}, {y}-{m}-{d})",
      "schema:contentUrl":f"https://openaq-data-archive.s3.amazonaws.com/records/csv.gz/locationid={locid}/year={y}/month={m}/location-{locid}-{y}{m}{d}.csv.gz",
      "schema:encodingFormat":["text/csv","application/gzip"]},
     {"@type":["schema:WebAPI"],"schema:name":"OpenAQ v3 API","schema:serviceType":"OpenAQ v3",
      "schema:termsOfService":"https://docs.openaq.org/about/terms","schema:documentation":"https://docs.openaq.org/",
      "schema:potentialAction":[{"@type":["schema:SearchAction"],"schema:name":"Get location",
        "schema:target":{"@type":["schema:EntryPoint"],"schema:urlTemplate":f"https://api.openaq.org/v3/locations/{locid}","schema:httpMethod":["GET"],"schema:contentType":["application/json"]}}]}]
def local_csv_dist(folder, fname, desc):
    return {"@type":["schema:DataDownload"],"schema:name":fname,"schema:description":desc,
      "schema:contentUrl":"https://w3id.org/cdif/airquality/examples/"+folder+"/"+fname,"schema:encodingFormat":["text/csv"]}
# DOI identifies the whole FILTER dataset: propertyID = DOI scheme, value = bare DOI, url = resolvable.
FILTER_DOI={"@type":["schema:PropertyValue"],"schema:propertyID":"https://registry.identifiers.org/registry/doi",
            "schema:value":"10.6084/m9.figshare.27195720","schema:url":"https://doi.org/10.6084/m9.figshare.27195720"}
def filter_sameas(sensor_local_id):
    # the per-sensor local id within the FILTER dataset, as an alternate identifier (CDIF core: schema:sameAs = other identifiers)
    return [{"@type":["schema:PropertyValue"],"schema:propertyID":"https://w3id.org/cdif/airquality/vocab/filter-sensor-id",
             "schema:value":sensor_local_id}]

# --- datastructure: LongDataStructure for long/EAV CSV (OpenAQ S3 narrow format) ---
def _rv(sid, lid, pdt):
    return {"@type":["cdi:RepresentedVariable"],"@id":sid+"/rv/"+lid,"cdif:name":[lid],"cdif:hasIntendedDataType":pdt}
def long_structure(base, param_varids):
    # DDI-CDI LongDataStructure: exactly ONE Identifier + ONE VariableDescriptor + ONE VariableValue + 0+ Attributes.
    # The sampling location is the identifier; sensors_id/datetime/units/lat/lon are attributes qualifying the value
    # (as the vitals example models its timestamp as an AttributeComponent). The key composes id + descriptor + attrs.
    S=base+"/struct"
    comps=[{"@type":["cdi:IdentifierComponent"],"@id":S+"/comp/location_id","cdif:isDefinedBy_Variable":_rv(S,"location_id","xsd:string")},
      {"@type":["cdi:VariableDescriptorComponent"],"@id":S+"/comp/parameter","cdi:refersTo":{"@id":S+"/comp/value"},
        "cdif:isDefinedBy_DescriptorVariable":{"@type":["cdi:DescriptorVariable"],"@id":S+"/dv/parameter","cdif:name":["parameter"],
          "cdif:hasValuesFrom":{"@type":["cdi:DescriptorValueDomain"],"@id":S+"/vd/parameter",
            "cdif:takesValuesFrom":[{"cdif:value":tok,"cdif:isDefinedBy":{"@id":vid}} for tok,vid in param_varids.items()]}}},
      {"@type":["cdi:VariableValueComponent"],"@id":S+"/comp/value","cdif:isDefinedBy_Variable":_rv(S,"value","xsd:decimal")}]
    for lid,pdt in [("sensors_id","xsd:string"),("datetime","xsd:dateTime"),("units","xsd:string"),("lat","xsd:decimal"),("lon","xsd:decimal")]:
        comps.append({"@type":["cdi:AttributeComponent"],"@id":S+"/comp/"+lid,"cdif:qualifies":[{"@id":S+"/comp/value"}],"cdif:isDefinedBy_Variable":_rv(S,lid,pdt)})
    return {"@type":["cdi:LongDataStructure"],"@id":S,"cdi:has_DataStructureComponent":comps,
        "cdif:has_PrimaryKey":{"@type":["cdif:Key"],"@id":S+"/pk","cdif:isComposedOf":[
          {"@type":["cdi:ComponentPosition"],"cdi:indexes":{"@id":S+"/comp/"+c},"cdi:value":i+1} for i,c in enumerate(["location_id","parameter","sensors_id","datetime"])]}}

CONFIGS=[]

# ---------- 1. SMR PurpleAir (FILTER, correction empty) ----------
CONFIGS.append(dict(
 folder="SMR_PurpleAir", fname="PA179671-cdif.jsonld",
 id="aq:filter-PA179671-SMR",
 name="FILTER-processed PM2.5 — PurpleAir sensor PA179671 (San Marino)",
 desc="Hourly PM2.5 from PurpleAir low-cost sensor PA179671 (San Marino), harmonized and quality-controlled by the FILTER framework (Hassani et al. 2025, NILU). Raw PM2.5 + QC flags; corrected values are empty for this sensor (insufficient nearby reference stations). Dual-channel (A/B).",
 identifier=FILTER_DOI, sameAs=filter_sameas("PA179671"),
 classname="Low-cost air-quality sensor observations", classcode="low-cost-sensor",
 modified="2025-03-24", url="https://doi.org/10.6084/m9.figshare.27195720",
 measurementTechnique=[dterm("Optical particle counting (laser scattering)","https://w3id.org/cdif/airquality/vocab/measurement-method","OPC")],
 license=[CCBY], creator=FILTER_CREATORS, publisher=NILU,
 provider=[{"@type":["schema:Organization"],"schema:name":"PurpleAir"}],
 keywords=["air quality","low-cost sensor","PM2.5","PurpleAir","FILTER","San Marino"],
 variables=filter_vars("aq:filter-PA179671-SMR"), conformsExtra=["https://w3id.org/cdif/data_description/2.0"],
 dqv=FILTER_QC,
 spatial=[{"@type":["schema:Place"],"schema:name":"San Marino","schema:additionalType":["country"],"schema:identifier":"SM"}],
 temporal="2023-04-30/2023-12-31",
 distribution=[FIGSHARE, filter_csv_dist("SMR_PurpleAir","PA179671_A.csv","FILTER CSV, PurpleAir channel A","aq:filter-PA179671-SMR")],
 wasGeneratedBy=filter_activity(openair("PurpleAir sensor PA179671","PurpleAir","PurpleAir",
    [sensor("PMS5003 module (channel A)",[sensing_element("optical particle counter (A)","OPC","Optical particle counting")]),
     sensor("PMS5003 module (channel B)",[sensing_element("optical particle counter (B)","OPC","Optical particle counting")])])),
 wasDerivedFrom=filter_derived("PurpleAir","https://www2.purpleair.com/"),
 catalog={"@id":"https://citiobs.eu/data-products/","@type":["schema:DataCatalog"],"schema:name":"CitiObs Data Products","schema:url":"https://citiobs.eu/data-products/"},
))

# ---------- 2. CHE PurpleAir (FILTER, corrected + CI) ----------
CONFIGS.append(dict(
 folder="CHE_corrected", fname="PA112746-cdif.jsonld",
 id="aq:filter-PA112746-CHE",
 name="FILTER-processed PM2.5 (raw + corrected) — PurpleAir sensor PA112746 (Switzerland)",
 desc="Hourly raw and bias-corrected PM2.5 from PurpleAir low-cost sensor PA112746 (Switzerland), from the FILTER framework (Hassani et al. 2025, NILU). Corrected values carry a 95% confidence interval and multi-step QC flags. Dual-channel (A/B).",
 identifier=FILTER_DOI, sameAs=filter_sameas("PA112746"),
 classname="Low-cost air-quality sensor observations", classcode="low-cost-sensor",
 modified="2025-03-24", url="https://doi.org/10.6084/m9.figshare.27195720",
 measurementTechnique=[dterm("Optical particle counting (laser scattering)","https://w3id.org/cdif/airquality/vocab/measurement-method","OPC")],
 license=[CCBY], creator=FILTER_CREATORS, publisher=NILU,
 provider=[{"@type":["schema:Organization"],"schema:name":"PurpleAir"}],
 keywords=["air quality","low-cost sensor","PM2.5","PurpleAir","FILTER","bias correction","Switzerland"],
 variables=filter_vars("aq:filter-PA112746-CHE"), conformsExtra=["https://w3id.org/cdif/data_description/2.0"],
 dqv=FILTER_QC+[{"@type":["dqv:QualityMeasurement"],"dqv:isMeasurementOf":dterm("Correction improvement",QCVOC,"correction-improvement"),"dqv:value":"per-hour 0/1 flag: did the correction reduce normalized RMSE vs reference"}],
 spatial=[{"@type":["schema:Place"],"schema:name":"Switzerland","schema:additionalType":["country"],"schema:identifier":"CH"}],
 temporal="2022-08-14/2023-12-31",
 distribution=[FIGSHARE, filter_csv_dist("CHE_corrected","PA112746_A.csv","FILTER CSV, PurpleAir channel A (corrected)","aq:filter-PA112746-CHE")],
 wasGeneratedBy=filter_activity(openair("PurpleAir sensor PA112746","PurpleAir","PurpleAir",
    [sensor("PMS5003 module (channel A)",[sensing_element("optical particle counter (A)","OPC","Optical particle counting")]),
     sensor("PMS5003 module (channel B)",[sensing_element("optical particle counter (B)","OPC","Optical particle counting")])])),
 wasDerivedFrom=filter_derived("PurpleAir","https://www2.purpleair.com/"),
 catalog={"@id":"https://citiobs.eu/data-products/","@type":["schema:DataCatalog"],"schema:name":"CitiObs Data Products","schema:url":"https://citiobs.eu/data-products/"},
))

# ---------- 3. ALB Sensor.community (FILTER) ----------
CONFIGS.append(dict(
 folder="ALB_SensorCommunity", fname="SC8323-cdif.jsonld",
 id="aq:filter-SC8323-ALB",
 name="FILTER-processed PM2.5 — Sensor.community sensor SC8323 (Albania)",
 desc="Hourly PM2.5 from Sensor.community low-cost sensor SC8323 (location 1835, Albania), harmonized and QC'd by the FILTER framework (Hassani et al. 2025, NILU). Single-channel; corrected values empty for this sensor.",
 identifier=FILTER_DOI, sameAs=filter_sameas("SC8323_1835"),
 classname="Low-cost air-quality sensor observations", classcode="low-cost-sensor",
 modified="2025-03-24", url="https://doi.org/10.6084/m9.figshare.27195720",
 measurementTechnique=[dterm("Optical particle counting (laser scattering)","https://w3id.org/cdif/airquality/vocab/measurement-method","OPC")],
 license=[CCBY], creator=FILTER_CREATORS, publisher=NILU,
 provider=[{"@type":["schema:Organization"],"schema:name":"Sensor.community","schema:url":"https://sensor.community"}],
 keywords=["air quality","low-cost sensor","PM2.5","Sensor.community","FILTER","Albania"],
 variables=filter_vars("aq:filter-SC8323-ALB"), conformsExtra=["https://w3id.org/cdif/data_description/2.0"],
 dqv=FILTER_QC,
 spatial=[{"@type":["schema:Place"],"schema:name":"Albania","schema:additionalType":["country"],"schema:identifier":"AL"}],
 temporal="2018-08-30/2018-09-16",
 distribution=[FIGSHARE, filter_csv_dist("ALB_SensorCommunity","SC8323_1835.csv","FILTER CSV, Sensor.community sensor","aq:filter-SC8323-ALB")],
 wasGeneratedBy=filter_activity(openair("Sensor.community node SC8323","Sensor.community","SDS011 (class)",
    [sensor("SDS011 PM module",[sensing_element("optical particle counter","OPC","Optical particle counting")])])),
 wasDerivedFrom=filter_derived("Sensor.community","https://sensor.community"),
 catalog={"@id":"https://citiobs.eu/data-products/","@type":["schema:DataCatalog"],"schema:name":"CitiObs Data Products","schema:url":"https://citiobs.eu/data-products/"},
))

# ---------- 4. AirNow reference (2178) ----------
gases_ppm=["co","no","no2","nox","o3","so2"]
v_airnow=[var(f"v-2178-{g}",g,"ppm","ppm",pollutant(g.upper()),g.upper()) for g in gases_ppm]+[
  var("v-2178-pm25","pm25","µg/m³","ug",pollutant("PM2.5"),"PM2.5"),
  var("v-2178-pm10","pm10","µg/m³","ug",pollutant("PM10"),"PM10")]
CONFIGS.append(dict(
 folder="OpenAQ_reference_AirNow_US", fname="location-2178-cdif.jsonld", long=True, conformsExtra=["https://w3id.org/cdif/data_structure/2.0"],
 id="aq:openaq-loc-2178",
 name="Reference air-quality monitoring — Del Norte, Albuquerque NM (US EPA AirNow, OpenAQ 2178)",
 desc="Hourly reference-grade observations (CO, NO, NO2, NOx, O3, SO2 in ppm; PM10, PM2.5 in µg/m³) from the US EPA AirNow monitoring station 'Del Norte' in Albuquerque, New Mexico, harvested via OpenAQ. Government reference monitor (isMonitor = true).",
 identifier={"@type":["schema:PropertyValue"],"schema:propertyID":"https://openaq.org","schema:value":"2178","schema:url":"https://api.openaq.org/v3/locations/2178"},
 classname="Reference-grade monitor observations", classcode="reference-monitor",
 modified="2026-11-25", url="https://explore.openaq.org/locations/2178",
 license=[{"@id":"https://www.usa.gov/government-works","@type":["schema:CreativeWork"],"schema:name":"US Public Domain (U.S. Government Work)","schema:url":"https://www.usa.gov/government-works"}],
 keywords=["air quality","reference monitor","US EPA","AirNow","criteria pollutants","Albuquerque"],
 publisher={"@type":["schema:GovernmentOrganization"],"schema:name":"Unknown Governmental Organization (data owner, per OpenAQ)"},
 provider=[{"@type":["schema:Organization"],"schema:name":"AirNow","schema:alternateName":"US EPA AirNow (OpenAQ provider)"}],
 variables=v_airnow,
 spatial=[{"@type":["schema:Place"],"schema:name":"Del Norte, Albuquerque","schema:geo":{"@type":["schema:GeoCoordinates"],"schema:latitude":35.1353,"schema:longitude":-106.584702}}],
 temporal="2016-03-06/2026-11-24",
 distribution=openaq_dist("2178","2016","09","23"),
 wasGeneratedBy=action("static","Stationary deployment",gov_monitor([
    sensor("Particulate analyser",[sensing_element("beta-ray attenuation detector","beta-attenuation","Beta-ray attenuation")],"BAM"),
    sensor("Nitrogen oxides analyser",[sensing_element("chemiluminescence detector","chemiluminescence","Chemiluminescence")]),
    sensor("Ozone analyser",[sensing_element("UV photometric detector","UV-photometry","UV photometry")]),
    sensor("Sulphur dioxide analyser",[sensing_element("UV fluorescence detector","UV-fluorescence","UV fluorescence")]),
    sensor("Carbon monoxide analyser",[sensing_element("NDIR detector","NDIR","Non-dispersive infrared")])]),"Del Norte, Albuquerque","America/Denver"),
 catalog={"@id":"https://openaq.org","@type":["schema:DataCatalog"],"schema:name":"OpenAQ","schema:url":"https://openaq.org"},
))

# ---------- 5. SINCA Chile reference (844) ----------
gases_ugm3=["co","no2","o3"]
v_sinca=[var(f"v-844-{g}",g,"µg/m³","ug",pollutant(g.upper()),g.upper()) for g in gases_ugm3]+[
  var("v-844-pm25","pm25","µg/m³","ug",pollutant("PM2.5"),"PM2.5"),
  var("v-844-pm10","pm10","µg/m³","ug",pollutant("PM10"),"PM10")]
CONFIGS.append(dict(
 folder="OpenAQ_reference_SINCA_Chile", fname="location-844-cdif.jsonld", long=True, conformsExtra=["https://w3id.org/cdif/data_structure/2.0"],
 id="aq:openaq-loc-844",
 name="Reference air-quality monitoring — Cerrillos (Chile SINCA, OpenAQ 844)",
 desc="Hourly reference-grade observations (CO, NO2, O3, PM10, PM2.5 — all in µg/m³) from the Chilean SINCA monitoring station 'Cerrillos', harvested via OpenAQ. Government reference monitor; note gases reported in µg/m³ (contrast with AirNow's ppm).",
 identifier={"@type":["schema:PropertyValue"],"schema:propertyID":"https://openaq.org","schema:value":"844","schema:url":"https://api.openaq.org/v3/locations/844"},
 classname="Reference-grade monitor observations", classcode="reference-monitor",
 modified="2026-11-25", url="https://explore.openaq.org/locations/844",
 conditionsOfAccess=["License not specified by the provider in OpenAQ; consult Chile SINCA (sinca.mma.gob.cl) terms of use before reuse."],
 keywords=["air quality","reference monitor","Chile","SINCA","criteria pollutants","Cerrillos"],
 publisher={"@type":["schema:GovernmentOrganization"],"schema:name":"Unknown Governmental Organization (data owner, per OpenAQ)"},
 provider=[{"@type":["schema:Organization"],"schema:name":"Chile - SINCA","schema:url":"https://sinca.mma.gob.cl"}],
 variables=v_sinca,
 spatial=[{"@type":["schema:Place"],"schema:name":"Cerrillos","schema:geo":{"@type":["schema:GeoCoordinates"],"schema:latitude":-33.492849,"schema:longitude":-70.719440}}],
 temporal="2016-01-30/2017-04-07",
 distribution=openaq_dist("844","2016","06","14"),
 wasGeneratedBy=action("static","Stationary deployment",gov_monitor([
    sensor("Particulate analyser",[sensing_element("beta-ray attenuation detector","beta-attenuation","Beta-ray attenuation")],"BAM"),
    sensor("Nitrogen oxides analyser",[sensing_element("chemiluminescence detector","chemiluminescence","Chemiluminescence")]),
    sensor("Ozone analyser",[sensing_element("UV photometric detector","UV-photometry","UV photometry")]),
    sensor("Carbon monoxide analyser",[sensing_element("NDIR detector","NDIR","Non-dispersive infrared")])]),"Cerrillos","America/Santiago"),
 catalog={"@id":"https://openaq.org","@type":["schema:DataCatalog"],"schema:name":"OpenAQ","schema:url":"https://openaq.org"},
))

# ---- build, write, validate ----
for cfg in CONFIGS:
    inst=build(cfg)
    out=os.path.join(BASE,cfg["folder"],cfg["fname"])
    with open(out,"w",encoding="utf-8") as fh: json.dump(inst,fh,indent=2,ensure_ascii=False)
    status="written"
    if SCHEMA is not None:
        v=jsonschema.Draft202012Validator(SCHEMA)
        errs=sorted(v.iter_errors(inst), key=lambda e:list(e.path))
        status=f"{len(errs)} error(s)"
        for e in errs[:6]: print("   ERR",cfg["fname"],list(e.path)[:4],"->",e.message[:110])
    print(f"{cfg['fname']:34} vars={len(cfg['variables'])} | {status}")
# patch the hand-written AirGradient instance with the same LongDataStructure
agf=os.path.join(BASE,"OpenAQ_lowcost_AirGradient_US","location-1236012-cdif.jsonld")
ag=json.load(open(agf,encoding="utf-8"))
pv={v["schema:name"]:v["@id"] for v in ag["schema:variableMeasured"]}
ag["schema:distribution"][0]["@type"]=["schema:DataDownload","cdi:TabularTextDataSet","cdi:PhysicalDataSet"]
ag["schema:distribution"][0]["cdi:isStructuredBy"]=long_structure(ag["@id"],pv)
cf=ag["schema:subjectOf"]["dcterms:conformsTo"]
if {"@id":"https://w3id.org/cdif/data_structure/2.0"} not in cf: cf.append({"@id":"https://w3id.org/cdif/data_structure/2.0"})
json.dump(ag,open(agf,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
print("patched AirGradient with LongDataStructure")
print("done")
