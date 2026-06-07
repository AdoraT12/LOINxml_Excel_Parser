import pandas as pd

from scripts.units import create_placeholder_unit
from scripts.config import EXCEL_FILE, PROPERTY_SET_COL, PROPERTY_SET_ND, SHEET_NAME, HEADER_ROW, OBJECT_COL, PROPERTY_COL, LPH_COL, FACHMODELL_COL, DATATYPE_COL, DESCRIPTION_COL, VALUE_TABLE_COL, UNIT_COL, FILTER_FACHMODELL
from scripts.helpers import match_lph, match_requirements, normalize_datatype
from scripts.classes import ObjectType, Property


def parse_excel():

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

    print("\n=== EXCEL COLUMNS ===")
    for col in df.columns:
        print(f"- {col}")
    print("=====================\n")

    print("\n=== FACHMODELL VALUES ===")

    for value in sorted(
        df[FACHMODELL_COL]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    ):
        print(repr(value))

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

        description = (
            None
            if pd.isna(row.get(DESCRIPTION_COL))
            else str(row.get(DESCRIPTION_COL)).strip()
        )

        possible_values = []

        if str(
            row.get(DATATYPE_COL, "")
        ).strip().lower() == "auswahlliste":

            vt = row.get(VALUE_TABLE_COL)

            if pd.notna(vt):

                possible_values = [
                    v.strip()
                    for v in str(vt).split("|")
                    if v.strip()
                ]

        # ----------------------------------------------------
        # UNIT
        # ----------------------------------------------------

        unit_obj = None

        unit_name = row.get(UNIT_COL)

        if pd.notna(unit_name):

            unit_name = str(unit_name).strip()

            unit_obj = create_placeholder_unit(
                unit_name
            )

            global_units[unit_name] = unit_obj

        # ----------------------------------------------------
        # PROPERTY
        # ----------------------------------------------------

        property_set_raw = row.get(PROPERTY_SET_COL)

        property_set = (
            None
            if pd.isna(property_set_raw)
            or str(property_set_raw).strip().lower() in {s.lower() for s in PROPERTY_SET_ND}
            else str(property_set_raw).strip()
        )

        prop = Property(
            name=prop_name,
            description=description,
            datatype=datatype,
            possible_values=possible_values,
            unit=unit_obj,
            property_set=property_set
        )

        current_object.properties.append(prop)

    return (
        objects,
        object_order,
        global_units
    )