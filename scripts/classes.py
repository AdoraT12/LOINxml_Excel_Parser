from dataclasses import dataclass, field
from scripts.utils import new_guid

@dataclass
class Dimension:

    name: str
    definition: str
    reference_uri: str
    exponents: dict

    guid: str = field(default_factory=new_guid)


@dataclass
class QuantityKind:

    name: str
    definition: str
    reference_uri: str
    dimension: Dimension

    guid: str = field(default_factory=new_guid)


@dataclass
class Unit:

    name: str
    definition: str
    symbol: str
    reference_uri: str
    quantity_kind: QuantityKind

    scale: str = "LINEAR"
    base: str = "TEN"
    coefficient: str = "1/1"
    offset: str = "0/1"

    guid: str = field(default_factory=new_guid)


@dataclass
class Property:

    name: str
    description: str
    datatype: str

    possible_values: list[str] = field(default_factory=list)
    unit: Unit | None = None

    guid: str = field(default_factory=new_guid)


@dataclass
class ObjectType:

    name: str

    parent: "ObjectType | None" = None
    properties: list["Property"] = field(default_factory=list)

    guid: str = field(default_factory=new_guid)