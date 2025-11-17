"""Advancement registration routines for the datapack generator."""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Iterable, Optional

from ..bucket import Bucket
from ..constants import (
    COMPONENT_CUSTOM_MODEL_DATA,
    MINECRAFT_NAMESPACE,
    TASTY_SUPPLIES_NAMESPACE,
)
from ..logger import log
from ..models.advancement import (
    Advancement,
    AdvancementIcon,
    AdvancementCriteria,
    ADVANCEMENT_TYPE,
)
from ..models.item import Item
from ..utils import ensure_namespace

_BACKGROUND = "minecraft:textures/gui/advancements/backgrounds/husbandry.png"


def _recipe_criteria(recipe_id: str) -> AdvancementCriteria:
    return AdvancementCriteria(
        trigger="minecraft:recipe_crafted",
        conditions={
            "recipe_id": ensure_namespace(
                recipe_id,
                TASTY_SUPPLIES_NAMESPACE,
                allow_tags=False,
            ),
        },
    )


def _item_condition(item: Item, extra_components: Optional[Dict[str, object]] = None) -> Dict[str, object]:
    components = {
        f"{MINECRAFT_NAMESPACE}:{COMPONENT_CUSTOM_MODEL_DATA}": {
            "strings": [f"{TASTY_SUPPLIES_NAMESPACE}/{item.name}"]
        }
    }
    if extra_components:
        components.update(deepcopy(extra_components))
    return {
        "items": f"{MINECRAFT_NAMESPACE}:{item.base_item}",
        "components": components,
    }


def _consume_item_criteria(item: Item) -> AdvancementCriteria:
    return AdvancementCriteria(
        trigger="minecraft:consume_item",
        conditions={
            "item": _item_condition(item),
        },
    )


def _require_item(bucket: Bucket, item_name: str) -> Item:
    item = bucket.get(item_name)
    if not item:
        raise ValueError(f"Missing item '{item_name}' required for advancement generation.")
    return item


def _optional_components(item: Item, keys: Iterable[str]) -> Optional[Dict[str, object]]:
    collected: Dict[str, object] = {}
    for key in keys:
        if key in item.components:
            collected[key] = deepcopy(item.components[key])
    return collected or None


def register_advancements(bucket: Bucket) -> None:
    """Register all advancements using the provided bucket content."""

    log.debug("Registering advancements via bucket")

    root = Advancement(
        advancement_id="tasty_supplies/root",
        title="Tasty Supplies",
        icon=AdvancementIcon("minecraft:cake"),
        criteria={"consumed_item": {"trigger": "minecraft:consume_item"}},
        requirements=[["consumed_item"]],
        background=_BACKGROUND,
        show_toast=False,
        announce_to_chat=False,
    )
    bucket.add_advancement(root, category="progression")

    nether = Advancement(
        advancement_id="tasty_supplies/nether",
        title="Nether",
        description="A portal to a whole range of new culinary possibilities",
        icon=AdvancementIcon("minecraft:red_nether_bricks"),
        criteria={
            "entered_nether": {
                "trigger": "minecraft:changed_dimension",
                "conditions": {"to": "minecraft:the_nether"},
            }
        },
        requirements=[["entered_nether"]],
        parent=root,
        background=_BACKGROUND,
    )
    bucket.add_advancement(nether, category="progression")

    apple_cider = _require_item(bucket, "apple_cider")
    glow_berry_custard = _require_item(bucket, "glow_berry_custard")
    hot_cocoa = _require_item(bucket, "hot_cocoa")
    melon_juice = _require_item(bucket, "melon_juice")

    barman_icon_components = _optional_components(apple_cider, ["potion_contents"])
    barman = Advancement(
        advancement_id="tasty_supplies/barman",
        title="Barman",
        description="Craft a drink",
        icon=AdvancementIcon(apple_cider, components=barman_icon_components),
        criteria={
            "apple_cider": _recipe_criteria("apple_cider"),
            "hot_cocoa": _recipe_criteria("hot_cocoa"),
            "glow_berry_custard": _recipe_criteria("glow_berry_custard"),
            "melon_juice": _recipe_criteria("melon_juice"),
        },
        requirements=[["apple_cider", "hot_cocoa", "glow_berry_custard", "melon_juice"]],
        parent=root,
        background=_BACKGROUND,
    )
    bucket.add_advancement(barman, category="crafting")

    comforting_icon_components = _optional_components(hot_cocoa, ["potion_contents"])
    comforting = Advancement(
        advancement_id="tasty_supplies/comforting",
        title="Comforting",
        description="Drink a hot cocoa",
        icon=AdvancementIcon(hot_cocoa, components=comforting_icon_components),
        criteria={"hot_cocoa": _consume_item_criteria(hot_cocoa)},
        requirements=[["hot_cocoa"]],
        parent=barman,
        background=_BACKGROUND,
    )
    bucket.add_advancement(comforting, category="consumption")

    flint_knife = _require_item(bucket, "flint_knife")
    iron_knife = _require_item(bucket, "iron_knife")
    golden_knife = _require_item(bucket, "golden_knife")
    diamond_knife = _require_item(bucket, "diamond_knife")
    netherite_knife = _require_item(bucket, "netherite_knife")

    knife = Advancement(
        advancement_id="tasty_supplies/knife",
        title="Small but handy",
        description="Craft a knife",
        icon=AdvancementIcon(flint_knife),
        criteria={
            "flint_knife": _recipe_criteria("flint_knife"),
            "iron_knife": _recipe_criteria("iron_knife"),
            "golden_knife": _recipe_criteria("golden_knife"),
            "diamond_knife": _recipe_criteria("diamond_knife"),
            "netherite_knife": _recipe_criteria("netherite_knife"),
        },
        requirements=[["flint_knife", "iron_knife", "golden_knife", "diamond_knife", "netherite_knife"]],
        parent=root,
        background=_BACKGROUND,
    )
    bucket.add_advancement(knife, category="crafting")

    all_knives = Advancement(
        advancement_id="tasty_supplies/all_knives",
        title="Cut them all",
        description="Craft all type of knives",
        icon=AdvancementIcon(netherite_knife),
        criteria=knife.criteria.copy(),
        requirements=[[key] for key in knife.criteria.keys()],
        parent=knife,
        background=_BACKGROUND,
        advancement_type=ADVANCEMENT_TYPE.CHALLENGE,
    )
    bucket.add_advancement(all_knives, category="challenges")

    nether_salad = _require_item(bucket, "nether_salad")
    fungus_skewer = _require_item(bucket, "fungus_skewer")
    magma_gelatin = _require_item(bucket, "magma_gelatin")
    warped_mutton = _require_item(bucket, "warped_mutton")

    fungus_among_us = Advancement(
        advancement_id="tasty_supplies/fungus_among_us",
        title="Fungus Amoung Us",
        description="Craft something with fungus",
        icon=AdvancementIcon("minecraft:crimson_fungus"),
        criteria={
            "nether_salad": _recipe_criteria("nether_salad"),
            "fungus_skewer": _recipe_criteria("fungus_skewer"),
            "fungus_skewer_reversed": _recipe_criteria("fungus_skewer_reversed"),
            "magma_gelatin": _recipe_criteria("magma_gelatin"),
            "warped_mutton": _recipe_criteria("warped_mutton"),
        },
        requirements=[["nether_salad", "fungus_skewer", "fungus_skewer_reversed", "magma_gelatin", "warped_mutton"]],
        parent=nether,
        background=_BACKGROUND,
    )
    bucket.add_advancement(fungus_among_us, category="nether")

    is_it_poisonous = Advancement(
        advancement_id="tasty_supplies/is_it_poisonous",
        title="Is this poisonous?",
        description="Eating food that makes you nauseous",
        icon=AdvancementIcon("minecraft:suspicious_stew"),
        criteria={
            "nether_salad": _consume_item_criteria(nether_salad),
            "fungus_skewer": _consume_item_criteria(fungus_skewer),
        },
        requirements=[["nether_salad", "fungus_skewer"]],
        parent=nether,
        background=_BACKGROUND,
    )
    bucket.add_advancement(is_it_poisonous, category="consumption")