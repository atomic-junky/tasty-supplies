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

_BACKGROUND = "minecraft:textures/block/bricks.png"


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


def _inventory_item_criteria(
    item: Item, extra_components: Optional[Dict[str, object]] = None
) -> AdvancementCriteria:
    return AdvancementCriteria(
        trigger="minecraft:inventory_changed",
        conditions={
            "items": [
                _item_condition(item, extra_components),
            ],
        },
    )


def _inventory_vanilla_item_criteria(item_id: str) -> AdvancementCriteria:
    return AdvancementCriteria(
        trigger="minecraft:inventory_changed",
        conditions={
            "items": [
                {
                    "items": [
                        ensure_namespace(
                            item_id,
                            MINECRAFT_NAMESPACE,
                        )
                    ]
                }
            ]
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
        description="A world of flavor awaits you!",
        icon=AdvancementIcon("minecraft:cake"),
        criteria={"seeds": {"conditions": {}, "trigger": "minecraft:inventory_changed"}},
        requirements=[["seeds"]],
        background=_BACKGROUND,
        show_toast=False,
        announce_to_chat=False,
    )
    bucket.add_advancement(root, category="progression")

    cutting_board = _require_item(bucket, "cutting_board")
    butter = _require_item(bucket, "butter")
    cooked_rice = _require_item(bucket, "cooked_rice")
    cheese_slice = _require_item(bucket, "cheese_slice")
    raw_cod_slice = _require_item(bucket, "raw_cod_slice")
    salmon_roll = _require_item(bucket, "salmon_roll")
    cod_roll = _require_item(bucket, "cod_roll")
    pie_crust = _require_item(bucket, "pie_crust")
    apple_pie = _require_item(bucket, "apple_pie")
    chocolate_pie = _require_item(bucket, "chocolate_pie")
    apple_pie_slice = _require_item(bucket, "apple_pie_slice")
    cherry_blossom_pie_slice = _require_item(bucket, "cherry_blossom_pie_slice")
    glow_berry_pie_slice = _require_item(bucket, "glow_berry_pie_slice")

    apple_cider = _require_item(bucket, "apple_cider")
    apple_cider_horn = _require_item(bucket, "apple_cider_horn")
    glow_berry_custard = _require_item(bucket, "glow_berry_custard")
    glow_berry_custard_horn = _require_item(bucket, "glow_berry_custard_horn")
    hot_cocoa = _require_item(bucket, "hot_cocoa")
    hot_cocoa_horn = _require_item(bucket, "hot_cocoa_horn")
    melon_juice = _require_item(bucket, "melon_juice")
    melon_juice_horn = _require_item(bucket, "melon_juice_horn")

    flint_knife = _require_item(bucket, "flint_knife")
    iron_knife = _require_item(bucket, "iron_knife")
    golden_knife = _require_item(bucket, "golden_knife")
    diamond_knife = _require_item(bucket, "diamond_knife")
    netherite_knife = _require_item(bucket, "netherite_knife")

    prep_station = Advancement(
        advancement_id="tasty_supplies/prep_station",
        title="Prep Station",
        description="Craft a cutting board to begin your culinary journey.",
        icon=AdvancementIcon(cutting_board),
        criteria={"cutting_board": _recipe_criteria("cutting_board")},
        requirements=[["cutting_board"]],
        parent=root,
        background=_BACKGROUND,
    )
    bucket.add_advancement(prep_station, category="progression")

    pantry_basics = Advancement(
        advancement_id="tasty_supplies/pantry_basics",
        title="Pantry Staples",
        description="Process milk and grains into butter and cooked rice.",
        icon=AdvancementIcon(butter),
        criteria={
            "butter": _recipe_criteria("butter"),
            "cooked_rice": _inventory_item_criteria(cooked_rice),
        },
        requirements=[["butter"], ["cooked_rice"]],
        parent=prep_station,
        background=_BACKGROUND,
    )
    bucket.add_advancement(pantry_basics, category="cooking")

    field_to_table = Advancement(
        advancement_id="tasty_supplies/field_to_table",
        title="Field to Table",
        description="Harvest staple crops to support your kitchen.",
        icon=AdvancementIcon("minecraft:hay_block"),
        criteria={
            "wheat": _inventory_vanilla_item_criteria("wheat"),
            "carrot": _inventory_vanilla_item_criteria("carrot"),
            "potato": _inventory_vanilla_item_criteria("potato"),
        },
        requirements=[["wheat"], ["carrot"], ["potato"]],
        parent=prep_station,
        background=_BACKGROUND,
        advancement_type=ADVANCEMENT_TYPE.GOAL,
    )
    bucket.add_advancement(field_to_table, category="challenges")

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
        parent=prep_station,
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

    precise_slices = Advancement(
        advancement_id="tasty_supplies/precise_slices",
        title="Precision Slicing",
        description="Slice cheese and fish on the cutting board.",
        icon=AdvancementIcon(cheese_slice),
        criteria={
            "cheese_slice": _inventory_item_criteria(cheese_slice),
            "raw_cod_slice": _inventory_item_criteria(raw_cod_slice),
        },
        requirements=[["cheese_slice"], ["raw_cod_slice"]],
        parent=knife,
        background=_BACKGROUND,
    )
    bucket.add_advancement(precise_slices, category="cooking")

    roll_with_it = Advancement(
        advancement_id="tasty_supplies/roll_with_it",
        title="Roll With It",
        description="Prepare both cod and salmon rolls.",
        icon=AdvancementIcon(salmon_roll),
        criteria={
            "salmon_roll": _recipe_criteria("salmon_roll"),
            "cod_roll": _recipe_criteria("cod_roll"),
        },
        requirements=[["salmon_roll"], ["cod_roll"]],
        parent=precise_slices,
        background=_BACKGROUND,
        advancement_type=ADVANCEMENT_TYPE.GOAL,
    )
    bucket.add_advancement(roll_with_it, category="meals")

    sweet_beginnings = Advancement(
        advancement_id="tasty_supplies/sweet_beginnings",
        title="Sweet Beginnings",
        description="Shape a pie crust ready for dessert work.",
        icon=AdvancementIcon(pie_crust),
        criteria={"pie_crust": _recipe_criteria("pie_crust")},
        requirements=[["pie_crust"]],
        parent=pantry_basics,
        background=_BACKGROUND,
    )
    bucket.add_advancement(sweet_beginnings, category="desserts")

    pie_party = Advancement(
        advancement_id="tasty_supplies/pie_party",
        title="Pie Party",
        description="Bake both apple and chocolate pies.",
        icon=AdvancementIcon(apple_pie),
        criteria={
            "apple_pie": _recipe_criteria("apple_pie"),
            "chocolate_pie": _recipe_criteria("chocolate_pie"),
        },
        requirements=[["apple_pie"], ["chocolate_pie"]],
        parent=sweet_beginnings,
        background=_BACKGROUND,
        advancement_type=ADVANCEMENT_TYPE.GOAL,
    )
    bucket.add_advancement(pie_party, category="desserts")

    dessert_sampler = Advancement(
        advancement_id="tasty_supplies/dessert_sampler",
        title="Dessert Sampler",
        description="Taste slices from your signature pies.",
        icon=AdvancementIcon(cherry_blossom_pie_slice),
        criteria={
            "apple_slice": _inventory_item_criteria(apple_pie_slice),
            "cherry_slice": _inventory_item_criteria(cherry_blossom_pie_slice),
            "glow_slice": _inventory_item_criteria(glow_berry_pie_slice),
        },
        requirements=[["apple_slice"], ["cherry_slice"], ["glow_slice"]],
        parent=pie_party,
        background=_BACKGROUND,
        advancement_type=ADVANCEMENT_TYPE.CHALLENGE,
    )
    bucket.add_advancement(dessert_sampler, category="desserts")

    apple_cider_icon_components = _optional_components(apple_cider, ["potion_contents"])
    brewery_basics = Advancement(
        advancement_id="tasty_supplies/brewery_basics",
        title="Brewery Basics",
        description="Brew your first specialty drink.",
        icon=AdvancementIcon(apple_cider, components=apple_cider_icon_components),
        criteria={"apple_cider": _recipe_criteria("apple_cider")},
        requirements=[["apple_cider"]],
        parent=root,
        background=_BACKGROUND,
    )
    bucket.add_advancement(brewery_basics, category="crafting")

    barman_criteria = {
        "apple_cider": _recipe_criteria("apple_cider"),
        "hot_cocoa": _recipe_criteria("hot_cocoa"),
        "glow_berry_custard": _recipe_criteria("glow_berry_custard"),
        "melon_juice": _recipe_criteria("melon_juice"),
    }
    barman = Advancement(
        advancement_id="tasty_supplies/barman",
        title="Barman",
        description="Craft every signature drink on the menu.",
        icon=AdvancementIcon(apple_cider, components=apple_cider_icon_components),
        criteria=barman_criteria,
        requirements=[[name] for name in barman_criteria.keys()],
        parent=brewery_basics,
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
        parent=brewery_basics,
        background=_BACKGROUND,
    )
    bucket.add_advancement(comforting, category="consumption")

    horn_of_plenty = Advancement(
        advancement_id="tasty_supplies/horn_of_plenty",
        title="Horn of Plenty",
        description="Fill goat horns with every beverage.",
        icon=AdvancementIcon("minecraft:goat_horn"),
        criteria={
            "apple_cider_horn": _recipe_criteria("apple_cider_horn"),
            "hot_cocoa_horn": _recipe_criteria("hot_cocoa_horn"),
            "glow_berry_custard_horn": _recipe_criteria("glow_berry_custard_horn"),
            "melon_juice_horn": _recipe_criteria("melon_juice_horn"),
        },
        requirements=[["apple_cider_horn"], ["hot_cocoa_horn"], ["glow_berry_custard_horn"], ["melon_juice_horn"]],
        parent=brewery_basics,
        background=_BACKGROUND,
        advancement_type=ADVANCEMENT_TYPE.GOAL,
    )
    bucket.add_advancement(horn_of_plenty, category="challenges")

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