# Build AQ_CDIF_profile_mapping.xlsx
# Crosswalk of AQ source metadata properties -> CDIF 7-profile properties.
# Row tuple: (source, group, variable, obligation, equiv_note, cdif_property, cdif_profile, status, note)
# status: mapped | partial | gap
#   mapped  = a CDIF property directly expresses it
#   partial = CDIF represents it only approximately / structurally (see note); counts as accounted-for but flagged
#   gap     = no CDIF property; basis for the AQ extension schema

R = []
def add(source, group, rows):
    for r in rows:
        R.append((source, group) + r)

# ======================= SOURCE 1: LCS proposed tables =======================
add("LCS-proposedtables","Measurement Location",[
 ("Measurement Location ID","M","StationEoICode","schema:spatialCoverage.schema:identifier","discovery","partial","Station id; CDIF has no first-class monitoring-location class"),
 ("CountryCode","M","CountryCode","schema:spatialCoverage.schema:name","discovery","partial","Country as Place; no addressCountry in CDIF Place"),
 ("Sampling Point Id (link)","M","","cdif:ForeignKey / cdi:ComponentPosition","datastructure","partial","Relational key between AQ tables, not a discovery property"),
 ("Latitude (decimal degrees)","M","Latitude","schema:spatialCoverage.schema:geo.schema:latitude","discovery","mapped",""),
 ("Longitude (decimal degrees)","M","Longitude","schema:spatialCoverage.schema:geo.schema:longitude","discovery","mapped",""),
 ("Lat/Lon accuracy","","","","","gap","Coordinate uncertainty; no CDIF property"),
])
add("LCS-proposedtables","Sampling Point",[
 ("Sampling Point Id","M","SamplingPointReferenceId","schema:identifier","core","partial","No sampling-point class in CDIF"),
 ("Sensor Device Id or Sensing Element Id (link)","M","","cdif:ForeignKey","datastructure","partial","Relational link"),
 ("CountryCode","M","CountryCode","schema:spatialCoverage.schema:name","discovery","partial","Country as Place"),
 ("PollutantId","M","PollutantId","schema:variableMeasured.schema:propertyID","discovery","mapped","Measured-variable concept id"),
 ("Sensor device name","Mav","","prov:wasGeneratedBy.prov:used","core","partial","Instrument as used entity; no device class"),
 ("Sensor device area","V","Measurement Station Area","","","gap","Micro-environment/area classification"),
 ("Measurement category","Mav","SamplingPointCategory","schema:keywords / schema:additionalType","core","partial","Traffic/industrial/background classification"),
 ("Latitude (decimal degrees)","M","Latitude","schema:spatialCoverage.schema:geo.schema:latitude","discovery","mapped",""),
 ("Longitude (decimal degrees)","M","Longitude","schema:spatialCoverage.schema:geo.schema:longitude","discovery","mapped",""),
 ("Lat/Lon accuracy","V","","","","gap","Coordinate uncertainty"),
 ("Method for Lat/Lon retrieval","Mav","","","","gap","Manual/automatic geolocation method"),
 ("Altitude above sea level (m)","V","Altitude","","","gap","CDIF Place.geo lacks elevation"),
 ("Height (m) / inlet height","Mav","Inlet Height","","","gap","Sensor inlet height above ground"),
 ("Nearest Building horizontal distance (m)","Mav","Building Distance","","","gap","Siting metadata"),
 ("Road Kerb horizontal distance (m)","Mav","Kerb Distance","","","gap","Siting metadata"),
 ("Emission source horizontal distance (m)","Mav","Emission Source Distance","","","gap","Siting metadata"),
 ("Contact person / Institution","M",'Table "Authority"',"schema:contributor (Role)","core","mapped","Person/Organization with roleName"),
])
add("LCS-proposedtables","Sensor Device",[
 ("Sampling Point Id (link)","M","","cdif:ForeignKey","datastructure","partial","Relational link"),
 ("Sensor Device Id","M","","prov:wasGeneratedBy.prov:used (Identifier)","core","partial","Device identity; no device class"),
 ("Sensing Element Id (link)","M","","cdif:ForeignKey","datastructure","partial","Relational link"),
 ("Company","V","","","","gap","Instrument manufacturer; no CDIF manufacturer property"),
 ("Sensor model","V","","","","gap","Instrument model"),
 ("Serial number","V","","","","gap","Device serial number"),
 ("Firmware version","V","","","","gap","Device firmware version"),
 ("Year of production","V","","","","gap","Device production year"),
])
add("LCS-proposedtables","Sensing Element",[
 ("Sensing Element Id","M","","","","gap","Device-component id; no CDIF class"),
 ("Sensor Device Id (link)","M","","cdif:ForeignKey","datastructure","partial","Relational link"),
 ("Sampling Point Id (link)","M","","cdif:ForeignKey","datastructure","partial","Relational link"),
 ("PollutantId","M","PollutantCode","schema:variableMeasured.schema:propertyID","discovery","mapped",""),
 ("Measurement Type","Mav","MeasurementType","schema:measurementTechnique","discovery","mapped","Automatic analyzer/active etc."),
 ("Measurement Equipment","Mav","Equipment","prov:wasGeneratedBy.prov:used","core","partial","Instrument used"),
 ("Measurement Method","Mav","Method","schema:measurementTechnique","discovery","mapped",""),
 ("Analytical Technique","Mav","AnalyticalTechnique","schema:measurementTechnique / schema:additionalType","discovery","mapped","Scientific principle"),
 ("Manufacturing batch/date","V","","","","gap","Component manufacturing provenance"),
 ("Deployment date/Replacement date","Mav","","","","gap","Element deployment/replacement date"),
 ("Last calibration date","Mav","","","","gap","Calibration provenance date"),
])
add("LCS-proposedtables","LowCostSensors Deployment",[
 ("Sensor Device Id or Sensing Element Id (link)","M","","cdif:ForeignKey","datastructure","partial","Relational link"),
 ("LCS Deployment ID","M","","schema:identifier","core","partial","Deployment ~ dataset/collection id"),
 ("Sampling Point Id (link)","M","","cdif:ForeignKey","datastructure","partial","Relational link"),
 ("Deployment Type","M","","schema:keywords / schema:additionalType","core","partial","Large-scale vs individual"),
 ("Deployment name","M","","schema:name","core","mapped","Deployment ~ dataset name"),
 ("Monitoring mode","M","","schema:additionalType","core","partial","Static vs mobile; no CDIF mobility flag"),
 ("Deployment objective","V","","schema:description","core","partial","Free-text objective"),
 ("Monitoring year","M","","schema:temporalCoverage","discovery","mapped",""),
])
add("LCS-proposedtables","Calibration",[
 ("Calibration Id","M","","prov:wasGeneratedBy (prov:Activity @id)","core","partial","Calibration activity id"),
 ("LCS Deployment ID (link)","M","","cdif:ForeignKey","datastructure","partial","Relational link"),
 ("Calibration type","M","","prov:wasGeneratedBy.prov:Activity","core","partial","Lab/Field/Co-location/Model"),
 ("Calibration duration","Mav","","","","gap","Continuous/fixed period"),
 ("Calibration date begin","Mav","","","","gap","Calibration-scoped date (not dataset temporal extent)"),
 ("Calibration date end","Mav","","","","gap","Calibration-scoped date"),
 ("Timezone","M","","","","gap","No CDIF timezone property (ISO8601 offset only)"),
 ("Location","V","","schema:spatialCoverage","discovery","partial","Calibration location"),
 ("Reference instrument type","Mav","","","","gap","Reference co-location instrument"),
 ("Reference instrument model","Mav","","","","gap","Reference instrument model"),
 ("Reference instrument uncertainty","Mav","","dqv:hasQualityMeasurement","discovery","partial","Reference uncertainty"),
 ("Relative humidity (considered?)","V","","","","gap","Calibration covariate flag"),
 ("Temperature (considered?)","V","","","","gap","Calibration covariate flag"),
 ("Pressure (considered?)","V","","","","gap","Calibration covariate flag"),
 ("Presence of condensation/fog","V","","","","gap","Calibration covariate flag"),
 ("Ozone cross-sensitivity","V","","","","gap","Calibration covariate flag"),
 ("Algorithm","Mav","","","","gap","Correction algorithm"),
 ("Drift correction","Mav","","","","gap","Drift correction flag"),
 ("Contact person / Institution","M","","schema:contributor (Role)","core","mapped",""),
])
add("LCS-proposedtables","LowCostSensors Measurements",[
 ("Sampling Point Id (link)","M","","cdi:IdentifierComponent / ForeignKey","datastructure","partial","Row key"),
 ("PollutantId","M","PollutantId","schema:variableMeasured.schema:propertyID","discovery","mapped",""),
 ("Calibration Id (link)","M","","cdi:AttributeComponent / ForeignKey","datastructure","partial","Row attribute/link"),
 ("DataAggregationProcessId","M","DataAggregationProcessId","","","gap","Aggregation process (P1D/P1M); no CDIF property"),
 ("Measurement start","M","Sampling time","schema:temporalCoverage / cdi:InstanceVariable","discovery","partial","Time dimension of the data"),
 ("Measurement end","M","Sampling time","schema:temporalCoverage / cdi:InstanceVariable","discovery","partial","Time dimension of the data"),
 ("Timezone","M","Timezone","","","gap","No CDIF timezone property"),
 ("Value","M","Value","schema:variableMeasured (MeasureComponent)","discovery","mapped","The measured value variable"),
 ("Unit","M","Unit","schema:variableMeasured.schema:unitText / unitCode","discovery","mapped",""),
 ("Validity","Mav","Validity","dqv:hasQualityMeasurement / cdi SentinelValueDomain","discovery","partial","QA flag 1/0/-1"),
 ("Verification","Mav","Verification","dqv:hasQualityMeasurement","discovery","partial","QC-done flag"),
 ("Data Capture","Mav","Data capture","dqv:hasQualityMeasurement","discovery","partial","Completeness %"),
 ("Time Coverage","V","Time coverage","dqv:hasQualityMeasurement","discovery","partial","Coverage %"),
 ("TimeResolution","V","Sampling interval","","","gap","Sensing frequency; no CDIF property"),
 ("Temperature (C)","Mav","PNSD-related","schema:variableMeasured","discovery","mapped","Co-measured variable"),
 ("Relative Humidity (%)","Mav","PNSD-related","schema:variableMeasured","discovery","mapped","Co-measured variable"),
 ("Latitude (decimal degrees)","M","","schema:spatialCoverage.schema:geo.schema:latitude","discovery","mapped",""),
 ("Longitude (decimal degrees)","M","","schema:spatialCoverage.schema:geo.schema:longitude","discovery","mapped",""),
 ("Documentation","Mav","Documentation","schema:relatedLink / schema:subjectOf","core","partial","Linked PDF documentation"),
])

# ======================= SOURCE 2: AirGradient =======================
add("AirGradient-annotated","intake header",[
 ("creator e-mail","","","schema:creator.schema:contactPoint.schema:email","core","mapped",""),
 ("point of contact agent","","","schema:contributor (Role, contact)","core","mapped",""),
 ("point of contact e-mail","","","schema:contributor.schema:contactPoint.schema:email","core","mapped",""),
 ("creator institution","","","schema:creator (Organization) / schema:affiliation","core","mapped",""),
 ("network name","","","schema:name / schema:provider.schema:name","core","mapped",""),
 ("contributor","","","schema:contributor","core","mapped",""),
 ("related link","","","schema:relatedLink / schema:url","core","mapped",""),
 ("variable measured","","","schema:variableMeasured","discovery","mapped",""),
 ("instrument manufacturer","","","","","gap","No CDIF manufacturer property"),
 ("instrument model","","","","","gap","Instrument model"),
 ("instrument part","","","","","gap","Embedded sensing element"),
 ("action process - calibration","","","prov:wasGeneratedBy (prov:Activity)","core","partial","Calibration method/link"),
 ("data quality - uncertainty","","","dqv:hasQualityMeasurement","discovery","mapped","Fit/uncertainty measure"),
 ("site description","","","schema:description / schema:spatialCoverage","core","partial","Deployment context"),
 ("description","","","schema:description","core","mapped",""),
 ("additional property","","","","","gap","schema:additionalProperty not in CDIF profile"),
 ("related link (sample file)","","","schema:distribution / schema:relatedLink","core","mapped",""),
 ("question","","","","","gap","Correspondence, not a metadata property"),
 ("time zone","","","","","gap","No CDIF timezone property"),
])

# ======================= SOURCE 3: OpenAQ API =======================
add("OpenAQ-API","Location",[
 ("id","","","schema:identifier","core","mapped",""),
 ("name","","","schema:name","core","mapped",""),
 ("locality","","","schema:spatialCoverage.schema:name","discovery","partial",""),
 ("timezone","","","","","gap","No CDIF timezone property"),
 ("country.code","","","schema:spatialCoverage.schema:name","discovery","partial",""),
 ("country.name","","","schema:spatialCoverage.schema:name","discovery","partial",""),
 ("owner.id","","","schema:publisher.schema:identifier","core","mapped",""),
 ("owner.name","","","schema:publisher.schema:name","core","mapped",""),
 ("provider.id","","","schema:provider.schema:identifier","core","mapped",""),
 ("provider.name","","","schema:provider.schema:name","core","mapped",""),
 ("isMobile","","","schema:additionalType","core","partial","Mobility flag; no CDIF property"),
 ("isMonitor","","","schema:additionalType","core","partial","Reference vs low-cost; no CDIF property"),
 ("instruments[].name","","","prov:wasGeneratedBy.prov:used","core","partial","Instrument"),
 ("sensors[].name","","","schema:variableMeasured.schema:name","discovery","mapped",""),
 ("sensors[].parameter","","","schema:variableMeasured.schema:propertyID","discovery","mapped",""),
 ("coordinates.latitude","","","schema:spatialCoverage.schema:geo.schema:latitude","discovery","mapped",""),
 ("coordinates.longitude","","","schema:spatialCoverage.schema:geo.schema:longitude","discovery","mapped",""),
 ("bounds","","","schema:spatialCoverage.schema:geo.schema:box","discovery","mapped",""),
 ("licenses[].name","","","schema:license","core","mapped",""),
 ("licenses[].attribution","","","schema:license (Reference) / odrl duty","access","partial","Attribution requirement"),
 ("licenses[].dateFrom","","","odrl:constraint (temporal)","access","partial","License validity start"),
 ("licenses[].dateTo","","","odrl:constraint (temporal)","access","partial","License validity end"),
 ("datetimeFirst","","","schema:temporalCoverage","discovery","mapped",""),
 ("datetimeLast","","","schema:temporalCoverage","discovery","mapped",""),
])
add("OpenAQ-API","Sensor",[
 ("id","","","schema:variableMeasured.@id","discovery","mapped",""),
 ("name","","","schema:variableMeasured.schema:name","discovery","mapped",""),
 ("parameter.name","","","schema:variableMeasured.schema:propertyID","discovery","mapped",""),
 ("parameter.units","","","schema:variableMeasured.schema:unitText","discovery","mapped",""),
 ("parameter.displayName","","","schema:variableMeasured.schema:alternateName","discovery","mapped",""),
 ("coverage","","","dqv:hasQualityMeasurement / cdif:statistics","datadescription","partial","Temporal coverage/completeness"),
 ("latest.value","","","","","gap","Latest reading (operational, not metadata)"),
 ("latest.datetime","","","schema:temporalCoverage","discovery","partial",""),
 ("summary.min","","","schema:variableMeasured.schema:minValue","discovery","mapped",""),
 ("summary.max","","","schema:variableMeasured.schema:maxValue","discovery","mapped",""),
 ("summary.avg","","","cdif:statistics (cdi:Statistics)","datadescription","partial","Mean over lifetime"),
])
add("OpenAQ-API","Parameter",[
 ("id","","","schema:variableMeasured.schema:propertyID (DefinedTerm.identifier)","discovery","mapped",""),
 ("name","","","schema:variableMeasured.schema:propertyID","discovery","mapped",""),
 ("units","","","schema:variableMeasured.schema:unitText / unitCode","discovery","mapped",""),
 ("displayName","","","schema:variableMeasured.schema:name (DefinedTerm.name)","discovery","mapped",""),
 ("description","","","schema:variableMeasured.schema:description","discovery","mapped",""),
])
add("OpenAQ-API","Measurement",[
 ("value","","","schema:variableMeasured (value)","discovery","mapped",""),
 ("parameter","","","schema:variableMeasured.schema:propertyID","discovery","mapped",""),
 ("period.label","","","","","gap","Aggregation label (raw/hourly)"),
 ("period.interval","","","","","gap","Aggregation interval; no CDIF property"),
 ("period.datetimeFrom","","","schema:temporalCoverage","discovery","mapped",""),
 ("period.datetimeTo","","","schema:temporalCoverage","discovery","mapped",""),
 ("coordinates","","","schema:spatialCoverage.schema:geo","discovery","mapped","Per-measurement coords (mobile)"),
 ("coverage.expectedCount","","","dqv:hasQualityMeasurement","discovery","partial",""),
 ("coverage.observedCount","","","dqv:hasQualityMeasurement","discovery","partial",""),
 ("coverage.percentComplete","","","dqv:hasQualityMeasurement","discovery","partial",""),
 ("summary.min","","","cdif:statistics","datadescription","partial",""),
 ("summary.median","","","cdif:statistics","datadescription","partial",""),
 ("summary.max","","","cdif:statistics","datadescription","partial",""),
 ("summary.sd","","","cdif:statistics","datadescription","partial",""),
])
add("OpenAQ-API","Instrument",[
 ("id","","","prov:wasGeneratedBy.prov:used (Identifier)","core","partial",""),
 ("name","","","prov:wasGeneratedBy.prov:used","core","partial",""),
 ("isMonitor","","","schema:additionalType","core","partial","Reference vs low-cost"),
 ("manufacturer.name","","","","","gap","No CDIF manufacturer property"),
])
add("OpenAQ-API","Manufacturer",[
 ("id","","","","","gap","No CDIF manufacturer class"),
 ("name","","","","","gap","No CDIF manufacturer class"),
 ("instruments[].name","","","prov:wasGeneratedBy.prov:used","core","partial",""),
])
add("OpenAQ-API","Owner",[
 ("id","","","schema:publisher.schema:identifier","core","mapped",""),
 ("name","","","schema:publisher.schema:name","core","mapped",""),
])
add("OpenAQ-API","Provider",[
 ("id","","","schema:provider.schema:identifier","core","mapped",""),
 ("name","","","schema:provider.schema:name","core","mapped",""),
 ("sourceName","","","schema:provider.schema:alternateName","core","partial",""),
 ("exportPrefix","","","","","gap","Internal export label"),
 ("datetimeAdded","","","schema:subjectOf.schema:sdDatePublished","core","partial",""),
 ("bbox","","","schema:spatialCoverage.schema:geo.schema:box","discovery","mapped",""),
])
add("OpenAQ-API","Country",[
 ("id","","","schema:spatialCoverage.schema:identifier","discovery","partial",""),
 ("code","","","schema:spatialCoverage.schema:name","discovery","partial",""),
 ("name","","","schema:spatialCoverage.schema:name","discovery","partial",""),
])
add("OpenAQ-API","License",[
 ("id","","","schema:license.schema:identifier","core","mapped",""),
 ("name","","","schema:license","core","mapped",""),
 ("commercialUseAllowed","","","odrl:permission (odrl:action commercialize)","access","mapped",""),
 ("attributionRequired","","","odrl:duty (odrl:action attribute)","access","mapped",""),
 ("shareAlikeRequired","","","odrl:duty (shareAlike)","access","mapped",""),
 ("modificationAllowed","","","odrl:permission (odrl:action modify)","access","mapped",""),
 ("redistributionAllowed","","","odrl:permission (odrl:action distribute)","access","mapped",""),
 ("sourceUrl","","","schema:license (url) / odrl:profile","core","mapped",""),
])
add("OpenAQ-S3csv","measurement row",[
 ("location_id","","","cdi:IdentifierComponent / schema:identifier","datastructure","partial",""),
 ("sensors_id","","","schema:variableMeasured.@id","discovery","partial",""),
 ("location","","","schema:spatialCoverage.schema:name","discovery","partial",""),
 ("datetime","","","schema:temporalCoverage / cdi:InstanceVariable","discovery","mapped",""),
 ("lat","","","schema:spatialCoverage.schema:geo.schema:latitude","discovery","mapped",""),
 ("lon","","","schema:spatialCoverage.schema:geo.schema:longitude","discovery","mapped",""),
 ("parameter","","","schema:variableMeasured.schema:propertyID","discovery","mapped",""),
 ("units","","","schema:variableMeasured.schema:unitText","discovery","mapped",""),
 ("value","","","schema:variableMeasured (value)","discovery","mapped",""),
])

# ======================= SOURCE 4: Sensor.community =======================
add("SensorCommunity-API","sensordata record",[
 ("software_version","","","","","gap","Firmware/software version of node"),
 ("age","","","","","gap","Data age (operational)"),
 ("timestamp","","","schema:temporalCoverage / cdi:InstanceVariable","discovery","mapped",""),
 ("sensordatavalues[].value_type","","","schema:variableMeasured.schema:propertyID","discovery","mapped",""),
 ("sensordatavalues[].value","","","schema:variableMeasured (value)","discovery","mapped",""),
 ("sensor.id","","","schema:identifier / prov:used","core","partial",""),
 ("sensor.pin","","","","","gap","Hardware pin assignment"),
 ("sensor.sensor_type.name","","","schema:measurementTechnique / prov:used","discovery","partial",""),
 ("sensor.sensor_type.manufacturer","","","","","gap","No CDIF manufacturer property"),
 ("location.id","","","schema:spatialCoverage.schema:identifier","discovery","partial",""),
 ("location.latitude","","","schema:spatialCoverage.schema:geo.schema:latitude","discovery","mapped",""),
 ("location.longitude","","","schema:spatialCoverage.schema:geo.schema:longitude","discovery","mapped",""),
 ("location.altitude","","","","","gap","CDIF Place.geo lacks elevation"),
 ("location.country","","","schema:spatialCoverage.schema:name","discovery","partial",""),
 ("location.indoor","","","schema:additionalType","core","partial","Indoor/outdoor flag; no CDIF property"),
])
add("SensorCommunity-archive","daily CSV (per sensor type)",[
 ("sensor_id","","","schema:identifier / cdi:IdentifierComponent","datastructure","partial",""),
 ("sensor_type","","","schema:measurementTechnique","discovery","partial",""),
 ("location","","","schema:spatialCoverage.schema:identifier","discovery","partial",""),
 ("lat","","","schema:spatialCoverage.schema:geo.schema:latitude","discovery","mapped",""),
 ("lon","","","schema:spatialCoverage.schema:geo.schema:longitude","discovery","mapped",""),
 ("timestamp","","","schema:temporalCoverage / cdi:InstanceVariable","discovery","mapped",""),
 ("P1 (PM10)","","","schema:variableMeasured","discovery","mapped",""),
 ("P2 (PM2.5)","","","schema:variableMeasured","discovery","mapped",""),
 ("durP1/ratioP1","","","","","gap","Sensor-internal diagnostic field"),
 ("temperature","","","schema:variableMeasured","discovery","mapped",""),
 ("humidity","","","schema:variableMeasured","discovery","mapped",""),
 ("pressure","","","schema:variableMeasured","discovery","mapped",""),
])

# ======================= SOURCE 5: FILTER sample data =======================
add("FILTER-sampledata","hourly CSV row",[
 ("hour_timestamp","","","schema:temporalCoverage / cdi:InstanceVariable","discovery","mapped",""),
 ("sensor_id","","","schema:identifier / cdi:IdentifierComponent","datastructure","partial",""),
 ("location","","","schema:spatialCoverage.schema:identifier","discovery","partial",""),
 ("raw_pm2_5","","","schema:variableMeasured (PM2.5 raw)","discovery","mapped",""),
 ("spread","","","dqv:hasQualityMeasurement","discovery","partial","Hour representativeness 1/2/3"),
 ("raw_qc (5-flag string)","","","dqv:hasQualityMeasurement / cdi SentinelValueDomain","discovery","partial","5-step QC flag string"),
 ("corrected_pm2_5","","","schema:variableMeasured (PM2.5 corrected)","discovery","mapped",""),
 ("corrected_ci_down","","","cdif:statistics","datadescription","partial","Lower CI bound"),
 ("corrected_ci_up","","","cdif:statistics","datadescription","partial","Upper CI bound"),
 ("correction_improvement","","","dqv:hasQualityMeasurement","discovery","partial","nRMSE-reduction flag"),
 ("corrected_qc (5-flag string)","","","dqv:hasQualityMeasurement","discovery","partial","5-step QC flag string"),
])

# ------------------- REVIEW + MODELING reclassification pass -----------------
# Keyed by (source, group, variable). Values: (cdif_property, profile, status, note)
INSTR = "prov:wasGeneratedBy.schema:instrument"          # Instrument building block (schemaorgProperties/instrument)
SITE  = "prov:wasGeneratedBy.schema:location.schema:Place.schema:additionalProperty"  # site-context PropertyValue
NEST  = "needs nested hasPart (instrument>sensor>sensingElement) OR sensor hasProperty sensingElement — Instrument bblock caps hasPart at 1 level"
IBB   = "core+instrument-bb"

INSTRUMENT_MAP = {
 # clean Instrument-bblock properties -> mapped
 ("LCS-proposedtables","Sampling Point","Sensor device name"): (INSTR+".schema:name",IBB,"mapped","Instrument bblock name"),
 ("LCS-proposedtables","Sensor Device","Sensor Device Id"): (INSTR+".schema:identifier",IBB,"mapped","Instrument identifier"),
 ("LCS-proposedtables","Sensor Device","Company"): (INSTR+".schema:manufacturer.schema:name",IBB,"mapped","Instrument manufacturer (Organization)"),
 ("LCS-proposedtables","Sensor Device","Sensor model"): (INSTR+".schema:model.schema:name",IBB,"mapped","Instrument ProductModel name"),
 ("LCS-proposedtables","Sensor Device","Serial number"): (INSTR+".schema:identifier (PropertyValue, serial)",IBB,"mapped","Serial as structured Identifier"),
 ("LCS-proposedtables","Sensor Device","Firmware version"): (INSTR+".schema:additionalProperty (firmware)",IBB,"mapped","Soft-typed PropertyValue on Instrument"),
 ("LCS-proposedtables","Sensor Device","Year of production"): (INSTR+".schema:validFrom / schema:additionalProperty",IBB,"partial","Commission date or soft-typed property"),
 ("LCS-proposedtables","Sensing Element","Sensing Element Id"): (INSTR+".schema:hasPart[sensor].schema:hasPart[sensingElement].@id",IBB,"partial",NEST),
 ("LCS-proposedtables","Sensing Element","Measurement Equipment"): (INSTR+".schema:hasPart.schema:name (sensing element)",IBB,"partial",NEST),
 ("LCS-proposedtables","Sensing Element","Manufacturing batch/date"): (INSTR+".schema:additionalProperty",IBB,"partial","Soft-typed property on sensing element"),
 ("LCS-proposedtables","Sensing Element","Deployment date/Replacement date"): (INSTR+".schema:validFrom / schema:validThrough",IBB,"mapped","Commission / decommission dates"),
 ("LCS-proposedtables","Sensing Element","Last calibration date"): (INSTR+".schema:additionalProperty (calibration info)",IBB,"partial","Instrument bblock additionalProperty: 'calibration information'"),
 ("AirGradient-annotated","intake header","instrument manufacturer"): (INSTR+".schema:manufacturer.schema:name",IBB,"mapped",""),
 ("AirGradient-annotated","intake header","instrument model"): (INSTR+".schema:model.schema:name",IBB,"mapped",""),
 ("AirGradient-annotated","intake header","instrument part"): (INSTR+".schema:hasPart",IBB,"partial",NEST),
 ("OpenAQ-API","Location","instruments[].name"): (INSTR+".schema:name",IBB,"mapped",""),
 ("OpenAQ-API","Instrument","id"): (INSTR+".schema:identifier",IBB,"mapped",""),
 ("OpenAQ-API","Instrument","name"): (INSTR+".schema:name",IBB,"mapped",""),
 ("OpenAQ-API","Instrument","manufacturer.name"): (INSTR+".schema:manufacturer.schema:name",IBB,"mapped",""),
 ("OpenAQ-API","Manufacturer","id"): (INSTR+".schema:manufacturer.schema:identifier",IBB,"mapped",""),
 ("OpenAQ-API","Manufacturer","name"): (INSTR+".schema:manufacturer.schema:name",IBB,"mapped",""),
 ("OpenAQ-API","Manufacturer","instruments[].name"): (INSTR+".schema:name",IBB,"mapped",""),
 ("SensorCommunity-API","sensordata record","sensor.id"): (INSTR+".schema:identifier",IBB,"mapped",""),
 ("SensorCommunity-API","sensordata record","sensor.sensor_type.name"): (INSTR+".schema:model.schema:name / schema:additionalType",IBB,"mapped","Sensor type as model/category"),
 ("SensorCommunity-API","sensordata record","sensor.sensor_type.manufacturer"): (INSTR+".schema:manufacturer.schema:name",IBB,"mapped",""),
 ("SensorCommunity-API","sensordata record","sensor.pin"): (INSTR+".schema:additionalProperty",IBB,"partial","Soft-typed hardware property"),
 ("SensorCommunity-API","sensordata record","software_version"): (INSTR+".schema:additionalProperty (firmware/software)",IBB,"partial","Soft-typed property"),
}
SITING_MAP = {  # site-context description -> prov activity's location Place additionalProperty (per modeling note)
 ("LCS-proposedtables","Sampling Point","Nearest Building horizontal distance (m)"): (SITE,"core(prov)","mapped","Site-context PropertyValue on generating activity's Place"),
 ("LCS-proposedtables","Sampling Point","Road Kerb horizontal distance (m)"): (SITE,"core(prov)","mapped","Site-context PropertyValue on generating activity's Place"),
 ("LCS-proposedtables","Sampling Point","Emission source horizontal distance (m)"): (SITE,"core(prov)","mapped","Site-context PropertyValue on generating activity's Place"),
 ("LCS-proposedtables","Sampling Point","Height (m) / inlet height"): (SITE,"core(prov)","mapped","Inlet height as site-context PropertyValue on Place"),
}
UPGRADE_MAPPED = {
 ("OpenAQ-API","Sensor","summary.avg"),
 ("OpenAQ-API","Measurement","summary.min"),
 ("OpenAQ-API","Measurement","summary.median"),
 ("OpenAQ-API","Measurement","summary.max"),
 ("OpenAQ-API","Measurement","summary.sd"),
}
GAP_QC_FLAGS = {
 ("FILTER-sampledata","hourly CSV row","raw_qc (5-flag string)"),
 ("FILTER-sampledata","hourly CSV row","correction_improvement"),
 ("FILTER-sampledata","hourly CSV row","corrected_qc (5-flag string)"),
}
GAP_CI = {
 ("FILTER-sampledata","hourly CSV row","corrected_ci_down"),
 ("FILTER-sampledata","hourly CSV row","corrected_ci_up"),
}
GAP_NOTE = {
 "E":"Multi-step QC flag string / correction diagnostic; exceeds dqv single-value model. Extension.",
 "F":"Per-value confidence interval; not a standard summary statistic. Extension.",
}

# Harvested example values (source, group, variable) -> example string
EXAMPLES = {
 ("LCS-proposedtables","Measurement Location","Measurement Location ID"):"ML_Stavanger_NO0052A_Langgata2",
 ("LCS-proposedtables","Measurement Location","Latitude (decimal degrees)"):"59.91 (example)",
 ("LCS-proposedtables","Sampling Point","Sampling Point Id"):"SP_Stavanger_Sensirion_005_1",
 ("LCS-proposedtables","Sampling Point","PollutantId"):"PM10 / temperature",
 ("LCS-proposedtables","Sampling Point","Sensor device name"):"Sensirion",
 ("LCS-proposedtables","Sampling Point","Nearest Building horizontal distance (m)"):"0 (attached to wall)",
 ("LCS-proposedtables","Sensor Device","Sensor Device Id"):"SD_Sensirion_SEN55_20240518-001284_2.4.1",
 ("LCS-proposedtables","Sensor Device","Company"):"Sensirion",
 ("LCS-proposedtables","Sensor Device","Sensor model"):"Sensirion SEN55",
 ("LCS-proposedtables","Sensor Device","Serial number"):"20240518-001284",
 ("LCS-proposedtables","Sensor Device","Firmware version"):"2.4.1",
 ("LCS-proposedtables","Sensing Element","Sensing Element Id"):"SE_SPS30_OPC_20260212_1",
 ("LCS-proposedtables","Sensing Element","PollutantId"):"PM2.5",
 ("LCS-proposedtables","Sensing Element","Measurement Type"):"automatic analyzer/active",
 ("LCS-proposedtables","Sensing Element","Measurement Equipment"):"SPS30 / SPS40",
 ("LCS-proposedtables","Sensing Element","Measurement Method"):"Laser scattering / OPC",
 ("LCS-proposedtables","Sensing Element","Analytical Technique"):"light scattering (PM); electrochemical (NO2,O3,CO)",
 ("LCS-proposedtables","LowCostSensors Deployment","LCS Deployment ID"):"DEP_static_neighborhood_CITIZENSEE_2025_1",
 ("LCS-proposedtables","LowCostSensors Deployment","Deployment Type"):"static / mobile",
 ("LCS-proposedtables","LowCostSensors Deployment","Monitoring mode"):"static",
 ("LCS-proposedtables","Calibration","Calibration Id"):"CAL_co-location_CITISENSEE_2026_2",
 ("LCS-proposedtables","Calibration","Calibration type"):"co-location / lab / field / model",
 ("LCS-proposedtables","LowCostSensors Measurements","Value"):"6.45",
 ("LCS-proposedtables","LowCostSensors Measurements","Unit"):"ug/m3",
 ("AirGradient-annotated","intake header","creator e-mail"):"anika.krause@airgradient.com",
 ("AirGradient-annotated","intake header","point of contact agent"):"Anika Krause; Achim Haug",
 ("AirGradient-annotated","intake header","creator institution"):"AirGradient",
 ("AirGradient-annotated","intake header","network name"):"AirGradient",
 ("AirGradient-annotated","intake header","related link"):"www.airgradient.com",
 ("AirGradient-annotated","intake header","variable measured"):"PM2.5, RH, Temp, CO2",
 ("AirGradient-annotated","intake header","instrument manufacturer"):"AirGradient",
 ("AirGradient-annotated","intake header","instrument model"):"AirGradient OpenAir (O-1PST, O-1PPT)",
 ("AirGradient-annotated","intake header","instrument part"):"embedded sensors (see airgradient.com)",
 ("AirGradient-annotated","intake header","action process - calibration"):"PM2.5: EPA correction",
 ("AirGradient-annotated","intake header","data quality - uncertainty"):"airgradient.com/documentation/calibration-algorithms/",
 ("OpenAQ-API","Location","id"):"2178",
 ("OpenAQ-API","Location","name"):"Del Norte",
 ("OpenAQ-API","Location","locality"):"Albuquerque",
 ("OpenAQ-API","Location","timezone"):"America/Denver",
 ("OpenAQ-API","Location","country.code"):"US",
 ("OpenAQ-API","Location","country.name"):"United States",
 ("OpenAQ-API","Location","owner.name"):"Unknown Governmental Organization / SEEN/SEEDS",
 ("OpenAQ-API","Location","provider.name"):"AirNow / AirGradient",
 ("OpenAQ-API","Location","isMobile"):"false",
 ("OpenAQ-API","Location","isMonitor"):"true (AirNow) / false (AirGradient)",
 ("OpenAQ-API","Location","instruments[].name"):"Government Monitor / Unknown AirGradient Sensor",
 ("OpenAQ-API","Location","sensors[].name"):"co ppm / pm1 ug/m3",
 ("OpenAQ-API","Location","coordinates.latitude"):"35.1353",
 ("OpenAQ-API","Location","coordinates.longitude"):"-106.584702",
 ("OpenAQ-API","Location","licenses[].name"):"US Public Domain / CC BY 4.0",
 ("OpenAQ-API","Location","datetimeFirst"):"2016-03-06T20:00:00Z",
 ("OpenAQ-API","Parameter","name"):"pm25",
 ("OpenAQ-API","Parameter","units"):"ug/m3 / ppm",
 ("OpenAQ-API","Parameter","displayName"):"PM2.5",
 ("OpenAQ-API","Instrument","name"):"Government Monitor",
 ("OpenAQ-API","Instrument","isMonitor"):"true",
 ("OpenAQ-API","Manufacturer","name"):"AirGradient",
 ("OpenAQ-API","License","name"):"CC BY 4.0",
 ("OpenAQ-API","License","attributionRequired"):"true",
 ("OpenAQ-API","License","sourceUrl"):"https://creativecommons.org/licenses/by/4.0/",
 ("OpenAQ-S3csv","measurement row","location_id"):"2178",
 ("OpenAQ-S3csv","measurement row","sensors_id"):"3919",
 ("OpenAQ-S3csv","measurement row","location"):"Del Norte-2178",
 ("OpenAQ-S3csv","measurement row","datetime"):"2016-09-23T01:00:00-06:00",
 ("OpenAQ-S3csv","measurement row","lat"):"35.1353",
 ("OpenAQ-S3csv","measurement row","lon"):"-106.584702",
 ("OpenAQ-S3csv","measurement row","parameter"):"pm10",
 ("OpenAQ-S3csv","measurement row","units"):"ug/m3",
 ("OpenAQ-S3csv","measurement row","value"):"6.0",
 ("SensorCommunity-API","sensordata record","sensordatavalues[].value_type"):"SDS_P1 (PM10), SDS_P2 (PM2.5)",
 ("SensorCommunity-API","sensordata record","sensordatavalues[].value"):"26.83",
 ("SensorCommunity-API","sensordata record","sensor.sensor_type.name"):"SDS011",
 ("SensorCommunity-API","sensordata record","software_version"):"NRZ-2017-099",
 ("SensorCommunity-archive","daily CSV (per sensor type)","sensor_id"):"1835",
 ("SensorCommunity-archive","daily CSV (per sensor type)","location"):"SC8323",
 ("SensorCommunity-archive","daily CSV (per sensor type)","P2 (PM2.5)"):"40.15",
 ("SensorCommunity-archive","daily CSV (per sensor type)","timestamp"):"1535662800 (epoch) / UTC",
 ("FILTER-sampledata","hourly CSV row","hour_timestamp"):"1660471200 (=2022-08-14 10:00Z)",
 ("FILTER-sampledata","hourly CSV row","sensor_id"):"A (PurpleAir channel)",
 ("FILTER-sampledata","hourly CSV row","location"):"PA112746",
 ("FILTER-sampledata","hourly CSV row","raw_pm2_5"):"4.03",
 ("FILTER-sampledata","hourly CSV row","spread"):"3",
 ("FILTER-sampledata","hourly CSV row","raw_qc (5-flag string)"):"10330",
 ("FILTER-sampledata","hourly CSV row","corrected_pm2_5"):"6.44813",
 ("FILTER-sampledata","hourly CSV row","corrected_ci_down"):"4.50076",
 ("FILTER-sampledata","hourly CSV row","corrected_ci_up"):"8.3955",
 ("FILTER-sampledata","hourly CSV row","correction_improvement"):"1",
 ("FILTER-sampledata","hourly CSV row","corrected_qc (5-flag string)"):"10330",
}

_R=[]
for t in R:
    source,group,variable,oblig,equiv,cdif,profile,status,note = t
    key=(source,group,variable)
    if key in INSTRUMENT_MAP:
        cdif,profile,status,note = INSTRUMENT_MAP[key]
    elif key in SITING_MAP:
        cdif,profile,status,note = SITING_MAP[key]
    elif key in UPGRADE_MAPPED:
        status="mapped"; note=(note+"; cdif:statistics holds this").strip("; ")
    elif key in GAP_QC_FLAGS:
        status="gap"; note=GAP_NOTE["E"]; cdif=""; profile=""
    elif key in GAP_CI:
        status="gap"; note=GAP_NOTE["F"]; cdif=""; profile=""
    _R.append((source,group,variable,oblig,equiv,cdif,profile,status,note))
R=_R

# ----------------------------------------------------------------------------
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HEAD = ["Variable (source property)","Variable source","Source group / table","Obligation (LCS)","EEA/EU equivalent or note","CDIF property (target)","CDIF profile","Match status","Mapping note","Example value (harvested)"]
# reorder each R row -> header order + example lookup
def to_row(t):
    source,group,variable,oblig,equiv,cdif_prop,profile,status,note = t
    ex=EXAMPLES.get((source,group,variable),"")
    return [variable,source,group,oblig,equiv,cdif_prop,profile,status,note,ex]

rows=[to_row(t) for t in R]
wb=openpyxl.Workbook()

def style_sheet(ws, data, headers):
    ws.append(headers)
    for r in data: ws.append(r)
    hf=Font(bold=True,color="FFFFFF"); hfill=PatternFill("solid",fgColor="305496")
    for c in range(1,len(headers)+1):
        cell=ws.cell(1,c); cell.font=hf; cell.fill=hfill; cell.alignment=Alignment(vertical="center",wrap_text=True)
    ws.freeze_panes="A2"; ws.auto_filter.ref=ws.dimensions
    widths=[34,22,26,12,30,44,18,13,46,34]
    for i,w in enumerate(widths[:len(headers)],1): ws.column_dimensions[get_column_letter(i)].width=w
    # color status col (col 8)
    fills={"mapped":PatternFill("solid",fgColor="C6EFCE"),"partial":PatternFill("solid",fgColor="FFEB9C"),"gap":PatternFill("solid",fgColor="FFC7CE")}
    for ridx in range(2,ws.max_row+1):
        st=ws.cell(ridx,8).value
        if st in fills: ws.cell(ridx,8).fill=fills[st]
        ws.cell(ridx,1).alignment=Alignment(wrap_text=True,vertical="top")
        ws.cell(ridx,9).alignment=Alignment(wrap_text=True,vertical="top")
        ws.cell(ridx,6).alignment=Alignment(wrap_text=True,vertical="top")
        ws.cell(ridx,10).alignment=Alignment(wrap_text=True,vertical="top")

ws1=wb.active; ws1.title="Mapping"
style_sheet(ws1, rows, HEAD)

# Gaps sheet: status == gap
gap_rows=[r for r in rows if r[7]=="gap"]
ws2=wb.create_sheet("Gaps (extension schema)")
GAPHEAD=["Variable (source property)","Variable source","Source group / table","Obligation (LCS)","Why no CDIF match","Example value (harvested)"]
gdata=[[r[0],r[1],r[2],r[3],r[8],r[9]] for r in gap_rows]
ws2.append(GAPHEAD)
for r in gdata: ws2.append(r)
hf=Font(bold=True,color="FFFFFF"); hfill=PatternFill("solid",fgColor="9C0006")
for c in range(1,len(GAPHEAD)+1):
    cell=ws2.cell(1,c); cell.font=hf; cell.fill=hfill; cell.alignment=Alignment(vertical="center",wrap_text=True)
ws2.freeze_panes="A2"; ws2.auto_filter.ref=ws2.dimensions
for i,w in enumerate([34,22,26,12,52,32],1): ws2.column_dimensions[get_column_letter(i)].width=w
for ridx in range(2,ws2.max_row+1):
    ws2.cell(ridx,1).alignment=Alignment(wrap_text=True,vertical="top")
    ws2.cell(ridx,5).alignment=Alignment(wrap_text=True,vertical="top")
    ws2.cell(ridx,6).alignment=Alignment(wrap_text=True,vertical="top")

# Extension concepts sheet: consolidated themes
EXT=[
 ("Instrument nesting (sensor>sensingElement)","sensing element id, instrument part, measurement equipment (as sensing element)","LCS Sensing Element; AirGradient instrument part","MOSTLY COVERED by the Instrument bblock (prov:wasGeneratedBy.schema:instrument: name/manufacturer/model/identifier/validFrom/validThrough/additionalProperty). Only gap: the bblock caps schema:hasPart at ONE level. Extend to instrument>sensor>sensingElement, EITHER by allowing a 2nd hasPart level OR sensor hasProperty(additionalProperty) sensingElement."),
 ("Siting / micro-environment","sensor device area, measurement category, altitude/elevation, indoor/outdoor, lat/lon accuracy, geolocation method","LCS Sampling Point; Sensor.community location.altitude/indoor","Building/kerb/emission distances + inlet height now ROUTED to prov:wasGeneratedBy.schema:location.schema:Place.schema:additionalProperty (soft-typed PropertyValue). Remaining: define controlled propertyIDs (+ units) for area class, elevation, indoor/outdoor, coordinate accuracy/method."),
 ("Coordinate quality","lat/lon accuracy, method for lat/lon retrieval","LCS Measurement Location & Sampling Point","Geo-uncertainty + geolocation-method properties on spatialCoverage."),
 ("Calibration","calibration type/duration/dates, reference instrument type/model/uncertainty, covariate flags (RH/temp/pressure/condensation/O3), algorithm, drift correction","LCS Calibration; AirGradient action process-calibration","Calibration activity extension (prov:Activity subtype) with reference-instrument + covariate-consideration + algorithm properties."),
 ("QC / flags / correction","Validity, Verification, Data Capture, Time Coverage, spread, raw_qc/corrected_qc flag strings, correction_improvement, confidence intervals","LCS Measurements; FILTER sample data","Richer QC model than dqv single value: multi-step flag vocabularies + per-value confidence interval."),
 ("Aggregation / sampling","DataAggregationProcessId, TimeResolution, period.label/interval","LCS Measurements; OpenAQ Measurement.period","Aggregation-process + sampling-frequency properties for derived time series."),
 ("Timezone","timezone fields","LCS Calibration/Measurements; AirGradient; OpenAQ Location; (CDIF uses ISO8601 offsets)","Decide whether to add an explicit timezone property or require offset in datetimes."),
 ("Platform type flags","isMobile, isMonitor, monitoring mode, deployment type","OpenAQ Location/Instrument; LCS Deployment","Platform/station typing: mobility + reference-vs-lowcost + deployment-type as controlled terms."),
 ("Operational/non-metadata","latest value, data age, export prefix, question","OpenAQ Sensor/Provider; Sensor.community; AirGradient","Out of scope for discovery metadata (operational or correspondence fields)."),
]
ws3=wb.create_sheet("Extension concepts")
EH=["Extension concept","Example source properties","Where it appears","Suggested CDIF extension approach"]
ws3.append(EH)
for r in EXT: ws3.append(list(r))
hf=Font(bold=True,color="FFFFFF"); hfill=PatternFill("solid",fgColor="375623")
for c in range(1,len(EH)+1):
    cell=ws3.cell(1,c); cell.font=hf; cell.fill=hfill; cell.alignment=Alignment(vertical="center",wrap_text=True)
ws3.freeze_panes="A2"; ws3.auto_filter.ref=ws3.dimensions
for i,w in enumerate([26,46,42,56],1): ws3.column_dimensions[get_column_letter(i)].width=w
for ridx in range(2,ws3.max_row+1):
    for c in range(1,5): ws3.cell(ridx,c).alignment=Alignment(wrap_text=True,vertical="top")

import os
primary=r"C:\GithubC\CDIF\cdif-AirQualityAQ\AQ_CDIF_profile_mapping.xlsx"
try:
    wb.save(primary); out=primary
except PermissionError:
    out=r"C:\GithubC\CDIF\cdif-AirQualityAQ\AQ_CDIF_profile_mapping_reviewed.xlsx"
    wb.save(out)
    print("NOTE: primary file was locked (open in Excel); wrote reviewed copy instead.")

from collections import Counter
st=Counter(r[7] for r in rows)
pr=Counter(r[6] for r in rows if r[7]!="gap")
print("saved:",out)
print("total rows:",len(rows))
print("status:",dict(st))
print("profiles used (mapped+partial):",dict(pr))
print("gap rows:",len(gap_rows))
