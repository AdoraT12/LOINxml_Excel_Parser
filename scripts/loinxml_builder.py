from lxml import etree

from scripts.utils import new_guid, now
from scripts.helpers import create_multilang
from scripts.config import LOIN, NSMAP, DT, USE_EXTERNAL_UNITS_LIBRARY, UNITS_OUTPUT_XML, LANGUAGE

def build_loin_xml(objects, object_order):

    root = etree.Element(LOIN + "LevelOfInformationNeed", nsmap=NSMAP)

    spec = etree.SubElement(root, "Specification")
    spec.set(DT + "GUID", new_guid())
    spec.set("dateOfCreation", now())

    for obj_name in object_order:

        obj = objects[obj_name]

        if not obj.properties:
            continue

        created = now()

        spec_obj = etree.SubElement(spec, "SpecificationPerObjectType")
        spec_obj.set(DT + "GUID", obj.guid)
        spec_obj.set("dateOfCreation", created)

        create_multilang(
            spec_obj,
            DT + "Name",
            f"Spezifikation für {obj.name}"
        )

        object_type = etree.SubElement(spec_obj, "ObjectType")
        object_type.set(DT + "GUID", obj.guid)
        object_type.set("dateOfCreation", created)

        create_multilang(object_type, DT + "Name", obj.name)

        dict_ref = etree.SubElement(object_type, DT + "DictionaryRef")
        dict_ref.set(DT + "referenceURI", obj.dictionary_ref_uri)
        dict_ref.set(DT + "GUID", obj.dictionary_ref_guid)

        alpha = etree.SubElement(spec_obj, "AlphanumericalInformation")
        alpha.set(DT + "GUID", new_guid())

        # --- collect groups ---
        groups: dict[str, list] = {}   # group_name -> [prop, ...]

        for prop in obj.properties:
            if prop.property_set:
                groups.setdefault(prop.property_set, []).append(prop)

        for prop in obj.properties:
            prop_el = etree.SubElement(alpha, "Property")
            prop_el.set(DT + "GUID", prop.guid)
            prop_el.set("dateOfCreation", created)

            create_multilang(prop_el, DT + "Name", prop.name)

            if prop.description:
                create_multilang(prop_el, DT + "Description", prop.description)

            dtype = etree.SubElement(prop_el, DT + "DataType")
            dtype.set("name", prop.datatype)

            if prop.possible_values:
                vl = etree.SubElement(
                    etree.SubElement(dtype, DT + "PossibleValues"),
                    DT + "ValueList"
                )
                vl.set("language", LANGUAGE)
                for i, value in enumerate(prop.possible_values, start=1):
                    val = etree.SubElement(vl, DT + "Value")
                    val.set("order", str(i))
                    val.text = value

            if prop.unit:
                unit_ref = etree.SubElement(prop_el, DT + "UnitRef")
                unit_ref.set(DT + "GUID", prop.unit.guid)
                if USE_EXTERNAL_UNITS_LIBRARY:
                    unit_ref.set(DT + "referenceURI", f"file:{UNITS_OUTPUT_XML.name}")

        if groups:
            # filter out single-property groups
            groups = {k: v for k, v in groups.items() if len(v) > 1}

        if groups:
            groups_el = etree.SubElement(alpha, "GroupsOfProperties")

            for group_name, group_props in groups.items():
                gop = etree.SubElement(groups_el, "GroupOfProperties")
                gop.set(DT + "GUID", new_guid())
                gop.set("dateOfCreation", created)

                create_multilang(gop, DT + "Name", group_name)

                for prop in group_props:
                    ref = etree.SubElement(gop, DT + "HasPropertyRef")
                    ref.set(DT + "GUID", prop.guid)

        doc = etree.SubElement(spec_obj, "Documentation")
        doc.set(DT + "GUID", new_guid())

        geo = etree.SubElement(spec_obj, "GeometricalInformation")
        geo.set(DT + "GUID", new_guid())
        geo.set("placeholder", "true")

    geo_ref = etree.SubElement(spec, "GeoReferencing")

    return root