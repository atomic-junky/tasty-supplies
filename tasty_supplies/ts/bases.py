"""Vanilla items custom items are built on.

A recipe cannot match on components, so a custom item used as an ingredient
boils down to its support: two items sharing one become interchangeable, and a
support the player can craft makes the ingredient trivial to bypass. A support
also carries its own vanilla components, which ``components.DISABLED_COMPONENTS``
is there to drop.
"""

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Base:
    """A vanilla item used as a support."""

    id: str
    dedicated: bool = True
    """Rare and reserved for one item, so it is safe as an ingredient."""

    @staticmethod
    def of(value: Union["Base", str]) -> "Base":
        return value if isinstance(value, Base) else Base(value, dedicated=False)


BREAD = Base("bread", dedicated=False)
POTION = Base("potion", dedicated=False)
WOODEN_SWORD = Base("wooden_sword", dedicated=False)
LEATHER_HELMET = Base("leather_helmet", dedicated=False)
WRITTEN_BOOK = Base("written_book", dedicated=False)
RABBIT_STEW = Base("rabbit_stew", dedicated=False)
ARMOR_STAND = Base("armor_stand", dedicated=False)

BARNACLE_THONG = Base("guster_banner_pattern")
BUTTER = Base("poisonous_potato")
CHEESE_SLICE = Base("piglin_banner_pattern")
COOKED_BACON = Base("skull_banner_pattern")
COOKED_BARNACLE_THONG = Base("creeper_banner_pattern")
COOKED_RICE = Base("field_masoned_banner_pattern")
COOKED_TENTACLE = Base("mojang_banner_pattern")
FRIED_EGG = Base("piglin_banner_pattern")
GUARDIAN_TAIL = Base("flow_banner_pattern")
PASTA = Base("sheaf_pottery_sherd")
PIE_CRUST = Base("angler_pottery_sherd")
RAW_BACON = Base("archer_pottery_sherd")
RAW_COD_SLICE = Base("flower_banner_pattern")
RAW_PASTA = Base("skull_pottery_sherd")
RAW_SALMON_SLICE = Base("bordure_indented_banner_pattern")
RICE = Base("arms_up_pottery_sherd")
TENTACLE = Base("blade_pottery_sherd")
WHEAT_DOUGH = Base("snort_pottery_sherd")

DIAMOND_KNIFE = Base("disc_fragment_5")
DIAMOND_CLEAVER = Base("echo_shard")

TANKARD = Base("prismarine_crystals")
