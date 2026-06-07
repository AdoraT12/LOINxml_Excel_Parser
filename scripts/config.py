from pathlib import Path

# ============================================================
# INPUT 
# ============================================================

EXCEL_FILE = "Objektkatalog_Bundesbau_V1.0.xlsx"

SHEET_NAME = "Objektkatalog"
HEADER_ROW = 4

# ============================================================
# OUTPUT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
GENERATED_XML_DIR = BASE_DIR / "generated_xmls"

SPECIFICATION_XML_DIR = GENERATED_XML_DIR / "specification_xmls"
UNITS_XML_DIR = GENERATED_XML_DIR / "unit_xmls"

OUTPUT_XML = SPECIFICATION_XML_DIR / "08_06_arc_lph3.xml"
UNITS_OUTPUT_XML = UNITS_XML_DIR / "units_quantities_dimensions.xml"


USE_EXTERNAL_UNITS_LIBRARY = True # Set to True to save units ina spearate file to use as an external units library, False to include units in the same XML
UNITS_LIBRARY_URI = UNITS_OUTPUT_XML.resolve().as_uri()

LANGUAGE = "de"
UNITS_LANGUAGE = "en"

# ============================================================
# FILTERS
# ============================================================

FILTER_LPH = {"2", "3"}

FILTER_FACHMODELL = {
   s.upper() for s in[
   "ARC", "ARC/LA", "ARC/TA-SAN",
   "ARC/TWP", "ARC/TWP/ HLSK",
   "Architekt/BImA/TGAPlaner/\nErrichterfirma",
   "alles"
   ]
}

# FILTER_FACHMODELL = {
#     s.upper() for s in[
#     "ARC/TWP", "ARC/TWP/HLSK",
#     "ALLE"
#     ]
# }

#when both false, all properties are included regardless of BIMA and BW requirements
INCLUDE_BIMA = False
INCLUDE_BW = False

# ============================================================
# COLUMNS
# ============================================================

OBJECT_COL = "DE"
PROPERTY_COL = "Bezeichnung (deutsch)"
DESCRIPTION_COL = "Beschreibung"
DATATYPE_COL = "Wertetyp"
VALUE_TABLE_COL = "Wertetabelle"
UNIT_COL = "Einheit"

LPH_COL = "Verfügbarkeit   (LPH)"
FACHMODELL_COL = "Fachmodell/  Autor"

BIMA_COL = "Anforderung BImA"
BW_COL = "Anforderung Bw"

# ============================================================
# XML NAMESPACE
# ============================================================

NSMAP = {
    "loin": "https://iso.org/2024/LOIN",
    "dt": "https://standards.iso.org/iso/23387/ed-2/en/"
}

DT = "{https://standards.iso.org/iso/23387/ed-2/en/}"
LOIN = "{https://iso.org/2024/LOIN}"