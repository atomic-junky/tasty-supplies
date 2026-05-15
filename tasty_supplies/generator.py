"""Main generator for Tasty Supplies datapack.

This module orchestrates the generation of all items, recipes, and
related datapack resources.
"""

from typing import List

from beet import Function

from core import TSContext, Bucket, log, recipe_book
from core.recipes import *
from core.models import Category
from core.convert import convert_data


def generate(ctx: TSContext) -> None:
    """Generate all datapack content.

    Args:
        ctx: The Tasty Supplies context
    """
    bucket = Bucket()

    categories: List[Category] = [
        Sweets(bucket),
        Beverage(bucket),
        Meals(bucket),
        Ingredients(bucket),
        Tools(bucket),
        Equipements(bucket),
        Worksation(bucket),
    ]

    for category in categories:
        category.create_items()

    for category in categories:
        category.create_recipes()

    recipe_book.generate(ctx, bucket)

    bucket.register_all(ctx)
    convert_data(ctx, bucket)

    # TODO: Why is this here?
    cutting_board = bucket.get("cutting_board")
    if cutting_board:
        ctx.data["tasty_supplies:cutting_board/drop"] = Function(
            [f"summon minecraft:item ~ ~.5 ~ {{Item:{cutting_board.to_result()}}}"]
        )

    item_count = len(bucket.export_item_names())
    recipe_count = len(bucket.export_recipe_ids())

    log.info(f"Items generated")
    log.info(f"\t- {item_count} items")
    log.info(f"\t- {recipe_count} recipes")
