from pathlib import Path
from lxml import etree
from scripts.config import UNITS_OUTPUT_XML, DT

from scripts.units_library_builder import build_units_library


def update_units_library(global_units):

    # --------------------------------------------------
    # build library from current Excel run
    # --------------------------------------------------

    new_root = build_units_library(global_units)

    # --------------------------------------------------
    # first run -> no existing file
    # --------------------------------------------------

    if not Path(UNITS_OUTPUT_XML).exists():
        return new_root

    # --------------------------------------------------
    # load existing library
    # --------------------------------------------------

    existing_tree = etree.parse(str(UNITS_OUTPUT_XML))
    existing_root = existing_tree.getroot()

    # --------------------------------------------------
    # existing GUIDs
    # --------------------------------------------------

    existing_guids = {
        el.get(DT + "GUID")
        for el in existing_root.xpath(".//*[@dt:GUID]",
            namespaces={
                "dt":
                "https://standards.iso.org/iso/23387/ed-2/en/"
            }
        )
    }

    # --------------------------------------------------
    # append only missing entries
    # --------------------------------------------------

    for element in new_root:

        guid = element.get(DT + "GUID")

        if guid not in existing_guids:
            
            print("ADDING:", guid)
            
            existing_root.append(element)
            existing_guids.add(guid)

    return existing_root