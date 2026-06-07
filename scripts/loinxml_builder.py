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

        alpha = etree.SubElement(spec_obj, "AlphanumericalInformation")
        alpha.set(DT + "GUID", new_guid())

        for prop in obj.properties:

            prop_el = etree.SubElement(alpha, "Property")
            prop_el.set(DT + "GUID", prop.guid)
            prop_el.set("dateOfCreation", created)

            create_multilang(prop_el, DT + "Name", prop.name)

            if prop.description:
                create_multilang(
                    prop_el,
                    DT + "Description",
                    prop.description
                )

            dtype = etree.SubElement(prop_el, DT + "DataType")
            dtype.set("name", prop.datatype)

            if prop.possible_values:

                vl = etree.SubElement(
                    etree.SubElement(
                        dtype,
                        DT + "PossibleValues"
                    ),
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
                    unit_ref.set(
                        DT + "referenceURI",
                        f"file:{UNITS_OUTPUT_XML.name}"
                    )

        doc = etree.SubElement(spec_obj, "Documentation")
        doc.set("GUID", new_guid())

        geo = etree.SubElement(spec_obj, "GeometricalInformation")
        geo.set("GUID", new_guid())
        geo.set("placeholder", "true")

    geo_ref = etree.SubElement(spec, "GeoReferencing")
    geo_ref.set(DT + "GUID", new_guid())

    return root