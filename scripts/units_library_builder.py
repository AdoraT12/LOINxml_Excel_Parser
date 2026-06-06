from lxml import etree
from scripts.utils import new_guid, now
from scripts.config import DT, NSMAP, LANGUAGE
from scripts.helpers import create_multilang


def build_units_library(global_units):

    # ============================================================
    # BUILD UNITS LIBRARY XML
    # ============================================================

    lib_root = etree.Element(
        DT + "Library",
        nsmap=NSMAP
    )

    lib_root.set(DT + "GUID", new_guid())

    create_multilang(
        lib_root,
        DT + "Name",
        "Units Quantities Dimensions Library",
        lang=LANGUAGE
    )

    # ============================================================
    # GLOBAL QUANTITY KINDS
    # ============================================================

    written_qk = set()

    for unit in global_units.values():

        qk = unit.quantity_kind

        if qk.guid in written_qk:
            continue

        written_qk.add(qk.guid)

        qk_el = etree.SubElement(lib_root, "QuantityKind")

        qk_el.set(DT + "GUID", qk.guid)
        qk_el.set("dateOfCreation", now())

        create_multilang(qk_el, DT + "Name", qk.name)
        create_multilang(qk_el, DT + "Definition", qk.definition)

        ref = etree.SubElement(qk_el, DT + "ReferenceDocumentRef")
        ref.set(DT + "referenceURI", qk.reference_uri)

        dim_ref = etree.SubElement(qk_el, DT + "DimensionRef")
        dim_ref.set(DT + "GUID", qk.dimension.guid)

    # ============================================================
    # GLOBAL DIMENSIONS
    # ============================================================

    written_dimensions = set()

    for unit in global_units.values():

        dim = unit.quantity_kind.dimension

        if dim.guid in written_dimensions:
            continue

        written_dimensions.add(dim.guid)

        dim_el = etree.SubElement(lib_root, "Dimension")

        dim_el.set(DT + "GUID", dim.guid)
        dim_el.set("dateOfCreation", now())

        create_multilang(dim_el, DT + "Name", dim.name)
        create_multilang(dim_el, DT + "Definition", dim.definition)

        ref = etree.SubElement(dim_el, DT + "ReferenceDocumentRef")
        ref.set(DT + "referenceURI", dim.reference_uri)

        for exponent_name, value in dim.exponents.items():

            etree.SubElement(
                dim_el,
                DT + f"DimensionExponentFor{exponent_name}"
            ).text = str(value)

    # ============================================================
    # GLOBAL UNITS
    # ============================================================

    for unit in global_units.values():

        unit_el = etree.SubElement(lib_root, "Unit")

        unit_el.set(DT + "GUID", unit.guid)
        unit_el.set("dateOfCreation", now())

        create_multilang(unit_el, DT + "Name", unit.name)
        create_multilang(unit_el, DT + "Definition", unit.definition)
        create_multilang(unit_el, DT + "Symbol", unit.symbol)

        ref = etree.SubElement(unit_el, DT + "ReferenceDocumentRef")
        ref.set(DT + "referenceURI", unit.reference_uri)

        dim_ref = etree.SubElement(unit_el, DT + "DimensionRef")
        dim_ref.set(DT + "GUID", unit.quantity_kind.dimension.guid)

        etree.SubElement(unit_el, DT + "Scale").text = unit.scale
        etree.SubElement(unit_el, DT + "Base").text = unit.base
        etree.SubElement(unit_el, DT + "Coefficient").text = unit.coefficient
        etree.SubElement(unit_el, DT + "Offset").text = unit.offset

    return lib_root