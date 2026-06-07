import pandas as pd
from lxml import etree
from scripts.config import FILTER_LPH, INCLUDE_BIMA, INCLUDE_BW, BIMA_COL, BW_COL, LANGUAGE, UNITS_LANGUAGE 

def create_multilang(parent, tag, text, lang=None):

    if lang is None:
        lang = LANGUAGE

    el = etree.SubElement(parent, tag)
    el.text = "" if text is None else str(text)
    el.set("language", lang)

    return el

def create_unit_lang(parent, tag, text):
    return create_multilang(
        parent,
        tag,
        text,
        lang=UNITS_LANGUAGE
    )

# ============================================================
# FILTERING
# ============================================================

def match_lph(cell_value):

    # no filter -> accept everything
    if not FILTER_LPH:
        return True

    # treat empty excel cells as ""
    if pd.isna(cell_value):
        return "" in FILTER_LPH

    value = str(cell_value).strip()

    if value == "":
        return "" in FILTER_LPH

    values = [
        v.strip()
        for v in value.split("|")
        if v.strip()
    ]

    return any(v in FILTER_LPH for v in values)

def match_requirements(row):

    if not INCLUDE_BIMA and not INCLUDE_BW:
        return True

    bima = str(
        row.get(BIMA_COL, "")
    ).strip().lower()

    bw = str(
        row.get(BW_COL, "")
    ).strip().lower()

    bima_x = "x" in bima
    bw_x = "x" in bw

    # BOTH FILTERS ENABLED
    if INCLUDE_BIMA and INCLUDE_BW:
        return bima_x or bw_x

    # ONLY BIMA
    if INCLUDE_BIMA:
        return bima_x

    # ONLY BW
    if INCLUDE_BW:
        return bw_x

    return True

# ============================================================
# DATATYPE MAPPING
# ============================================================

def normalize_datatype(value):

    if pd.isna(value):
        return "STRING"

    v = str(value).strip().lower()

    mapping = {
        "freitext": "STRING",
        "bezeichnung": "STRING",
        "text": "STRING",
        "string": "STRING",

        "nummerisch": "REAL",
        "real": "REAL",
        "zahl": "REAL",

        "integer": "INTEGER",
        "ganzzahl": "INTEGER",

        "boolean": "BOOLEAN",
        "ja/nein": "BOOLEAN",

        "auswahlliste": "STRING",

        "datum": "DATETIME",

        "n.d.": "STRING",
        "": "STRING"
    }

    return mapping.get(v, "STRING")

