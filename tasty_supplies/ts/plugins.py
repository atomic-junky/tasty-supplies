"""The steps of the build, in the order ``beet.yml`` lists them."""

import logging

from beet import Context, Function, ItemModel, Model, PngFile
from beet import Recipe as RecipeFile
from beet.contrib.vanilla import Vanilla

from . import cookbook as cookbook_module
from . import templating
from .item import Item
from .recipe import Cut, as_result
from .registry import Registry
from .utils import to_snbt

logger = logging.getLogger(__name__)

NAMESPACE = "tasty_supplies"


def content(ctx: Context) -> None:
    """Read the catalog and make it available to the other steps."""

    registry = ctx.inject(Registry)
    registry.load()
    templating.register(ctx, registry)


def cookbook(ctx: Context) -> None:
    """Add the in-game recipe book, once every other item is known."""

    cookbook_module.generate(ctx, ctx.inject(Registry))


def emit(ctx: Context) -> None:
    """Write items, models and recipes into the packs."""

    registry = ctx.inject(Registry)
    ctx.assets.icon = PngFile(source_path=f"{NAMESPACE}/pack.png")

    assets = ctx.assets[NAMESPACE]
    functions = ctx.data[NAMESPACE].functions

    for item in registry.items.values():
        # A model shipped in src/ wins over the generated one.
        if not assets.models.get(f"item/{item.id}"):
            assets.models[f"item/{item.id}"] = Model(item.model)

        assets.item_models[item.id] = ItemModel(item.item_model)
        _add_model_case(ctx, item)

        if ctx.assets.textures.get(item.texture_path) is None:
            logger.warning("Missing texture for item %r.", item.id)

        functions[f"give/{item.id}"] = Function([f"give @s {item.give} 1"])

    for recipe in registry.recipes:
        if not isinstance(recipe, Cut):
            ctx.data[NAMESPACE].recipes[recipe.id] = RecipeFile(recipe.to_json())

    logger.info(
        "Generated %d items and %d recipes.", len(registry.items), len(registry.recipes)
    )


def _add_model_case(ctx: Context, item: Item) -> None:
    """Point the support item at our model when it carries our model data."""

    item_models = ctx.assets["minecraft"].item_models
    support = item.support.id

    if item_models.get(support) is None:
        item_models[support] = ItemModel(_select_on_model_data(ctx, support))

    model = item_models[support].data["model"]
    if model.get("cases") is None:
        raise ValueError(f"No model cases to extend on minecraft:items/{support}.")

    case = item.model_case
    if any(candidate["when"] == case["when"] for candidate in model["cases"]):
        logger.warning(
            "A model case for %r already exists on minecraft:items/%s.",
            item.id,
            support,
        )
        return

    model["cases"].append(case)


def _select_on_model_data(ctx: Context, support: str) -> dict:
    """A model that falls back to the vanilla one when no case matches."""

    vanilla_model = ctx.inject(Vanilla).assets.item_models.get(f"minecraft:{support}")
    if vanilla_model is None:
        raise ValueError(f"No vanilla item model for {support!r}.")

    return {
        "model": {
            "type": "minecraft:select",
            "property": "minecraft:custom_model_data",
            "cases": [],
            "fallback": vanilla_model.data["model"],
        }
    }


def cutting_board(ctx: Context) -> None:
    """The cutting board mechanic: one function per cut, plus the block drop."""

    registry = ctx.inject(Registry)
    dispatch = ctx.data[NAMESPACE].functions["cutting_board/cut_item"]

    for recipe in registry.recipes:
        if not isinstance(recipe, Cut):
            continue

        path = f"{NAMESPACE}:cutting_board/recipes/{recipe.id}"
        ctx.data[path] = Function([_summon(recipe.result_json), "kill @s"])
        dispatch.append(
            Function(
                f"execute if data entity @s item{_item_test(recipe.ingredient)}"
                f" run function {path}"
            )
        )

    board = registry.get("cutting_board")
    if board is not None:
        # Dropped when the block is broken, or when it cannot be placed.
        ctx.data[f"{NAMESPACE}:cutting_board/drop"] = Function([_summon(board.stack())])


def _summon(stack: dict) -> str:
    return f"summon minecraft:item ~ ~.5 ~ {{Item:{to_snbt(stack)}}}"


def _item_test(ingredient) -> str:
    """NBT test matching the item lying on the board."""

    if isinstance(ingredient, Item):
        return to_snbt(
            {
                "id": f"minecraft:{ingredient.support.id}",
                "components": {
                    "minecraft:custom_model_data": {
                        "strings": [f"{NAMESPACE}/{ingredient.id}"]
                    }
                },
            }
        )
    return to_snbt({"id": as_result(ingredient)["id"]})


def updater(ctx: Context) -> None:
    """Tables letting the pack replace items left over from an older version."""

    registry = ctx.inject(Registry)
    functions = ctx.data[NAMESPACE].functions

    known_hashes = functions["updater/check_sha1"]
    replace = functions["updater/replace_item"]

    for item in registry.items.values():
        known_hashes.append(
            "execute if data storage tasty_supplies:updater temp"
            f'{{hash: "{item.sha1}"}} run return 1'
        )
        replace.append(
            "$execute if data storage tasty_supplies:updater temp"
            f'{{item_name: "{item.id}"}} run item replace $(target) $(path)'
            f" with {item.give} $(count)"
        )
