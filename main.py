from lxml import etree

from scripts.config import OUTPUT_XML, UNITS_OUTPUT_XML, SPECIFICATION_XML_DIR, UNITS_XML_DIR
from scripts.parse_excel import parse_excel
from scripts.loinxml_builder import build_loin_xml
from scripts.units_library_builder import build_units_library

objects, object_order, global_units = parse_excel()

# ============================================================
# BUILD XML TREES
# ============================================================

root = build_loin_xml(
    objects,
    object_order
)

lib_root = build_units_library(
    global_units
)

# ============================================================
# SAVE LOIN XML
# ============================================================

SPECIFICATION_XML_DIR.mkdir(
    parents=True,
    exist_ok=True
)

tree = etree.ElementTree(root)

etree.indent(tree, space="    ")

tree.write(
    str(OUTPUT_XML),
    pretty_print=True,
    xml_declaration=True,
    encoding="utf-8"
)

print("DONE:", OUTPUT_XML)

# ============================================================
# SAVE UNITS LIBRARY
# ============================================================

UNITS_XML_DIR.mkdir(
    parents=True,
    exist_ok=True
)

lib_tree = etree.ElementTree(lib_root)

etree.indent(lib_tree, space="    ")

lib_tree.write(
    str(UNITS_OUTPUT_XML),
    pretty_print=True,
    xml_declaration=True,
    encoding="utf-8"
)

print("DONE:", UNITS_OUTPUT_XML)