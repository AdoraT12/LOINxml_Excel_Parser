import pandas as pd
import uuid
from lxml import etree
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

EXCEL_FILE = "Objektkatalog_Bundesbau_V1.0.xlsx"

SHEET_NAME = "Objektkatalog"
HEADER_ROW = 4

OUTPUT_XML = "test.xml"
UNITS_OUTPUT_XML = "units_quantities_dimensions_test.xml"

USE_EXTERNAL_UNITS_LIBRARY = True
UNITS_LIBRARY_URI = f"file:{UNITS_OUTPUT_XML}"

# ============================================================
# FILTERS
# ============================================================

FILTER_LPH = {"3"}

#FILTER_FACHMODELL = {
#    s.upper() for s in[
#    "ARC", "ARC/LA", "ARC/TA-SAN",
#    "ARC/TWP", "ARC/TWP/HLSK",
#    "ARCHITEKT/BIMA/TGAPLANER/ERRICHTERFIRMA",
#    "ALLE"
#    ]
#}

FILTER_FACHMODELL = {
    s.upper() for s in[
    "ARC/TWP", "ARC/TWP/HLSK",
    "ALLE"
    ]
}

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

# ============================================================
# HELPERS
# ============================================================

def new_guid():
    return str(uuid.uuid4())

def now():
    return datetime.now().isoformat()

def create_multilang(parent, tag, text, lang="de"):

    el = etree.SubElement(parent, tag)

    el.text = "" if text is None else str(text)

    el.set("language", lang)

    return el

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

# ============================================================
# DOMAIN CLASSES
# ============================================================

class Dimension:

    def __init__(
        self,
        name,
        definition,
        reference_uri,
        exponents
    ):

        self.guid = new_guid()

        self.name = name

        self.definition = definition

        self.reference_uri = reference_uri

        self.exponents = exponents


class QuantityKind:

    def __init__(
        self,
        name,
        definition,
        reference_uri,
        dimension
    ):

        self.guid = new_guid()

        self.name = name

        self.definition = definition

        self.reference_uri = reference_uri

        self.dimension = dimension


class Unit:

    def __init__(
        self,
        name,
        definition,
        symbol,
        reference_uri,
        quantity_kind,
        scale="LINEAR",
        base="TEN",
        coefficient="1/1",
        offset="0/1"
    ):

        self.guid = new_guid()

        self.name = name

        self.definition = definition

        self.symbol = symbol

        self.reference_uri = reference_uri

        self.quantity_kind = quantity_kind

        self.scale = scale

        self.base = base

        self.coefficient = coefficient

        self.offset = offset


class Property:

    def __init__(
        self,
        name,
        description,
        datatype,
        possible_values=None,
        unit=None
    ):

        self.guid = new_guid()

        self.name = name

        self.description = description

        self.datatype = datatype

        self.possible_values = possible_values or []

        self.unit = unit


class ObjectType:

    def __init__(self, name):

        self.guid = new_guid()

        self.name = name

        self.parent = None

        self.properties = []

DIMENSIONS = {

    "Length": Dimension(
        name="Length",
        definition="The dimension of length (L)",
        reference_uri="http://qudt.org/vocab/dimensionvector/A0E0L1I0M0H0T0D0",
        exponents={
            "Length": 1,
            "Mass": 0,
            "Time": 0,
            "ElectricCurrent": 0,
            "ThermodynamicTemperature": 0,
            "AmountOfSubstance": 0,
            "LuminousIntensity": 0
        }
    ),

    "Area": Dimension(
        name="Area",
        definition="The dimension of area (L²)",
        reference_uri="http://qudt.org/vocab/dimensionvector/A0E0L2I0M0H0T0D0",
        exponents={
            "Length": 2,
            "Mass": 0,
            "Time": 0,
            "ElectricCurrent": 0,
            "ThermodynamicTemperature": 0,
            "AmountOfSubstance": 0,
            "LuminousIntensity": 0
        }
    ),

    "Volume": Dimension(
        name="Volume",
        definition="The dimension of volume (L³)",
        reference_uri="http://qudt.org/vocab/dimensionvector/A0E0L3I0M0H0T0D0",
        exponents={
            "Length": 3,
            "Mass": 0,
            "Time": 0,
            "ElectricCurrent": 0,
            "ThermodynamicTemperature": 0,
            "AmountOfSubstance": 0,
            "LuminousIntensity": 0
        }
    )
}

QUANTITY_KINDS = {

    "Length": QuantityKind(
        name="Length",
        definition="The distance between two points in space",
        reference_uri="http://qudt.org/vocab/quantitykind/Length",
        dimension=DIMENSIONS["Length"]
    ),

    "Area": QuantityKind(
        name="Area",
        definition="The extent of a surface",
        reference_uri="http://qudt.org/vocab/quantitykind/Area",
        dimension=DIMENSIONS["Area"]
    ),

    "Volume": QuantityKind(
        name="Volume",
        definition="The amount of three-dimensional space",
        reference_uri="http://qudt.org/vocab/quantitykind/Volume",
        dimension=DIMENSIONS["Volume"]
    )
}

UNIT_LIBRARY = {

    "m": Unit(
        name="meter",
        definition="SI base unit of length",
        symbol="m",
        reference_uri="http://qudt.org/vocab/unit/M",
        quantity_kind=QUANTITY_KINDS["Length"]
    ),

    "mm": Unit(
        name="millimeter",
        definition="One thousandth of a meter",
        symbol="mm",
        reference_uri="http://qudt.org/vocab/unit/MilliM",
        quantity_kind=QUANTITY_KINDS["Length"],
        coefficient="1/1000"
    ),

    "m²": Unit(
        name="square meter",
        definition="SI unit of area",
        symbol="m²",
        reference_uri="http://qudt.org/vocab/unit/M2",
        quantity_kind=QUANTITY_KINDS["Area"]
    ),

    "m³": Unit(
        name="cubic meter",
        definition="SI unit of volume",
        symbol="m³",
        reference_uri="http://qudt.org/vocab/unit/M3",
        quantity_kind=QUANTITY_KINDS["Volume"]
    )
}

def create_placeholder_unit(unit_name):

    # avoid duplicates
    if unit_name in UNIT_LIBRARY:
        return UNIT_LIBRARY[unit_name]

    # --------------------------------------------
    # placeholder dimension
    # --------------------------------------------

    dim = Dimension(
        name=f"{unit_name}_Dimension",
        definition="TODO: PLACEHOLDER DEFINITION",
        reference_uri="TODO: PLACEHOLDER URI",
        exponents={
            "Length": 0,
            "Mass": 0,
            "Time": 0,
            "ElectricCurrent": 0,
            "ThermodynamicTemperature": 0,
            "AmountOfSubstance": 0,
            "LuminousIntensity": 0
        }
    )

    # --------------------------------------------
    # placeholder quantity kind
    # --------------------------------------------

    qk = QuantityKind(
        name=f"{unit_name}",
        definition="TODO:PLACEHOLDER DEFINITION",
        reference_uri="TODO: PLACEHOLDER URI",
        dimension=dim
    )

    # --------------------------------------------
    # placeholder unit
    # --------------------------------------------

    unit = Unit(
        name=unit_name,
        definition="TODO: PLACEHOLDER DEFINITION",
        symbol=unit_name,
        reference_uri="TODO: PLACEHOLDER URI",
        quantity_kind=qk
    )

    UNIT_LIBRARY[unit_name] = unit

    return unit

# ============================================================
# LOAD EXCEL
# ============================================================

df = pd.read_excel(
    EXCEL_FILE,
    sheet_name=SHEET_NAME,
    header=HEADER_ROW
)

df.columns = (
    df.columns.astype(str)
    .str.replace("\n", " ", regex=False)
    .str.replace("\r", " ", regex=False)
    .str.replace("\xa0", " ", regex=False)
    .str.strip()
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


objects = {}
object_order = []

global_units = {}

current_object = None

# ============================================================
# PARSE EXCEL
# ============================================================

for _, row in df.iterrows():

    object_name = row.get(OBJECT_COL)

    # ----------------------------------------------------
    # OBJECT ROW
    # ----------------------------------------------------

    is_object_row = (
        pd.notna(object_name)
        and str(object_name).strip() != ""
    )

    if is_object_row:

        # object rows only use requirement filtering
        if not match_requirements(row):
            current_object = None
            continue

        object_name = str(object_name).strip()

        if object_name not in objects:

            obj = ObjectType(object_name)

            objects[object_name] = obj

            object_order.append(object_name)

        current_object = objects[object_name]

        continue

    # ----------------------------------------------------
    # PROPERTY ROW
    # ----------------------------------------------------

    if current_object is None:
        continue

    # property filtering
    if not (
        match_lph(row[LPH_COL])
        and str(row[FACHMODELL_COL]).strip().upper()
            in FILTER_FACHMODELL
        and match_requirements(row)
    ):
        continue

    prop_name = row.get(PROPERTY_COL)

    if pd.isna(prop_name):
        continue

    prop_name = str(prop_name).strip()

    if prop_name == "" or prop_name.lower() == "n.d.":
        continue

    datatype = normalize_datatype(
        row.get(DATATYPE_COL)
    )

    description = row.get(DESCRIPTION_COL)

    possible_values = []

    if str(row.get(DATATYPE_COL, "")).strip().lower() == "auswahlliste":

        vt = row.get(VALUE_TABLE_COL)

        if pd.notna(vt):

            possible_values = [
                v.strip()
                for v in str(vt).split("|")
                if v.strip()
            ]

    # --------------------------------------------------------
    # UNIT
    # --------------------------------------------------------

    unit_obj = None

    unit_name = row.get(UNIT_COL)

    if pd.notna(unit_name):

        unit_name = str(unit_name).strip()

        unit_obj = create_placeholder_unit(unit_name)

        global_units[unit_name] = unit_obj

    # --------------------------------------------------------
    # PROPERTY
    # --------------------------------------------------------

    prop = Property(
        name=prop_name,
        description=description,
        datatype=datatype,
        possible_values=possible_values,
        unit=unit_obj
    )

    current_object.properties.append(prop)

# ============================================================
# BUILD XML
# ============================================================

root = etree.Element(
    LOIN + "LevelOfInformationNeed",
    nsmap=NSMAP
)

spec = etree.SubElement(root, "Specification")

spec.set(DT + "GUID", new_guid())
spec.set("dateOfCreation", now())

# ============================================================
# SPECIFICATION PER OBJECT TYPE
# ============================================================

for obj_name in object_order:

    obj = objects[obj_name]

    # ---------------------------------------------------------------------
    # SKIP OBJECTS WITHOUT ALPHANUMERICAL INFORMATION FOR THE GIVEN FILTERS
    # ---------------------------------------------------------------------

    if not obj.properties:
        continue

    created = now()

    spec_obj = etree.SubElement(
        spec,
        "SpecificationPerObjectType"
    )

    spec_obj.set(DT + "GUID", obj.guid)
    spec_obj.set("dateOfCreation", created)

    create_multilang(
        spec_obj,
        DT + "Name",
        f"Spezifikation für {obj.name}"
    )

    object_type = etree.SubElement(
        spec_obj,
        "ObjectType"
    )
    object_type.set(DT + "GUID", obj.guid)
    object_type.set("dateOfCreation", created)

    create_multilang(
        object_type,
        DT + "Name",
        obj.name
    )

    # ========================================================
    # Properties
    # ========================================================

    if obj.properties:

        alpha = etree.SubElement(
            spec_obj,
            "AlphanumericalInformation"
        )
        alpha.set(DT + "GUID", new_guid())

        for prop in obj.properties:

            prop_el = etree.SubElement(
                alpha,
                "Property"
            )
            prop_el.set(DT + "GUID", prop.guid)
            prop_el.set("dateOfCreation", created)

            create_multilang(prop_el, DT + "Name", prop.name)

            if prop.description:
                create_multilang(prop_el, DT + "Description", prop.description)

            # -----------------------------
            # DataType
            # -----------------------------
            dtype = etree.SubElement(
                prop_el,
                DT + "DataType"
            )

            dtype.set("name", prop.datatype)

            # enum values
            if prop.possible_values:

                pv = etree.SubElement(dtype, DT + "PossibleValues")
                vl = etree.SubElement(pv, DT + "ValueList")
                vl.set("language", "de")

                for i, v in enumerate(prop.possible_values, 1):

                    val = etree.SubElement(vl, DT + "Value")
                    val.set("order", str(i))
                    val.text = v

            # unit
            if prop.unit:

                unit_ref = etree.SubElement(prop_el, DT + "UnitRef")

                unit_ref.set(DT + "GUID", prop.unit.guid)

                if USE_EXTERNAL_UNITS_LIBRARY:
                    unit_ref.set(DT + "referenceURI", UNITS_LIBRARY_URI)

    # ========================================================
    # EMPTY EXTENSION BLOCKS PER OBJECT TYPE
    # ========================================================

    doc = etree.SubElement(spec_obj, "Documentation")
    doc.set("GUID", new_guid())

    geo = etree.SubElement(spec_obj, "GeometricalInformation")
    geo.set("GUID", new_guid())
    geo.set("placeholder", "false")

geo_ref = etree.SubElement(spec, "GeoReferencing")
geo_ref.set(DT + "GUID", new_guid()) 

# ============================================================
# BUILD UNITS LIBRARY XML
# ============================================================

lib_root = etree.Element(
    DT + "Library",
    nsmap={
        "loin": "https://iso.org/2024/LOIN",
        "dt": "https://standards.iso.org/iso/23387/ed-2/en/"
    }
)

lib_root.set(DT + "GUID", new_guid())

create_multilang(
    lib_root,
    DT + "Name",
    "Units Quantities Dimensions Library",
    lang="en"
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

    qk_el = etree.SubElement(
        lib_root,
        "QuantityKind"
    )

    qk_el.set(DT + "GUID", qk.guid)

    qk_el.set(
        "dateOfCreation",
        now()
    )

    create_multilang(
        qk_el,
        DT + "Name",
        qk.name
    )

    create_multilang(
        qk_el,
        DT + "Definition",
        qk.definition
    )

    ref = etree.SubElement(
        qk_el,
        DT + "ReferenceDocumentRef"
    )

    ref.set(
        DT + "referenceURI",
        qk.reference_uri
    )

    dim_ref = etree.SubElement(
        qk_el,
        DT + "DimensionRef"
    )

    dim_ref.set(
        DT + "GUID",
        qk.dimension.guid
    )

# ============================================================
# GLOBAL DIMENSIONS
# ============================================================

written_dimensions = set()

for unit in global_units.values():

    dim = unit.quantity_kind.dimension

    if dim.guid in written_dimensions:
        continue

    written_dimensions.add(dim.guid)

    dim_el = etree.SubElement(
        lib_root,
        "Dimension"
    )

    dim_el.set(DT + "GUID", dim.guid)

    dim_el.set(
        "dateOfCreation",
        now()
    )

    create_multilang(
        dim_el,
        DT + "Name",
        dim.name
    )

    create_multilang(
        dim_el,
        DT + "Definition",
        dim.definition
    )

    ref = etree.SubElement(
        dim_el,
        DT + "ReferenceDocumentRef"
    )

    ref.set(
        DT + "referenceURI",
        dim.reference_uri
    )

    etree.SubElement(
        dim_el,
        DT + "DimensionExponentForAmountOfSubstance"
    ).text = str(dim.exponents["AmountOfSubstance"])

    etree.SubElement(
        dim_el,
        DT + "DimensionExponentForElectricCurrent"
    ).text = str(dim.exponents["ElectricCurrent"])

    etree.SubElement(
        dim_el,
        DT + "DimensionExponentForLength"
    ).text = str(dim.exponents["Length"])

    etree.SubElement(
        dim_el,
        DT + "DimensionExponentForLuminousIntensity"
    ).text = str(dim.exponents["LuminousIntensity"])

    etree.SubElement(
        dim_el,
        DT + "DimensionExponentForMass"
    ).text = str(dim.exponents["Mass"])

    etree.SubElement(
        dim_el,
        DT + "DimensionExponentForThermodynamicTemperature"
    ).text = str(dim.exponents["ThermodynamicTemperature"])

    etree.SubElement(
        dim_el,
        DT + "DimensionExponentForTime"
    ).text = str(dim.exponents["Time"])

# ============================================================
# GLOBAL UNITS
# ============================================================

for unit in global_units.values():

    unit_el = etree.SubElement(
        lib_root,
        "Unit"
    )

    unit_el.set(DT + "GUID", unit.guid)

    unit_el.set(
        "dateOfCreation",
        now()
    )

    create_multilang(
        unit_el,
        DT + "Name",
        unit.name
    )

    create_multilang(
        unit_el,
        DT + "Definition",
        unit.definition
    )

    ref = etree.SubElement(
        unit_el,
        DT + "ReferenceDocumentRef"
    )

    ref.set(
        DT + "referenceURI",
        unit.reference_uri
    )

    create_multilang(
        unit_el,
        DT + "Symbol",
        unit.symbol
    )

    dim_ref = etree.SubElement(
        unit_el,
        DT + "DimensionRef"
    )

    dim_ref.set(
        DT + "GUID",
        unit.quantity_kind.dimension.guid
    )

    etree.SubElement(
        unit_el,
        DT + "Scale"
    ).text = unit.scale

    etree.SubElement(
        unit_el,
        DT + "Base"
    ).text = unit.base

    etree.SubElement(
        unit_el,
        DT + "Coefficient"
    ).text = unit.coefficient

    etree.SubElement(
        unit_el,
        DT + "Offset"
    ).text = unit.offset

# ============================================================
# SAVE XML
# ============================================================

tree = etree.ElementTree(root)
etree.indent(tree, space="    ")

tree.write(
    OUTPUT_XML,
    pretty_print=True,
    xml_declaration=True,
    encoding="utf-8"
)

print("DONE:", OUTPUT_XML)

# ============================================================
# SAVE UNITS LIBRARY
# ============================================================

lib_tree = etree.ElementTree(lib_root)

etree.indent(lib_tree, space="    ")

lib_tree.write(
    UNITS_OUTPUT_XML,
    pretty_print=True,
    xml_declaration=True,
    encoding="utf-8"
)

print("DONE:", UNITS_OUTPUT_XML)