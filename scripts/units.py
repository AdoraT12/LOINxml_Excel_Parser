from scripts.classes import Dimension, QuantityKind, Unit

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
        definition="TODO: PLACEHOLDER DEFINITION",
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

