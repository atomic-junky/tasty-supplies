import os
from typing import List
from beet import Font, Texture

from ..models import TSContext, Item, Recipe, ShapelessRecipe, Rarity
from ..bucket import Bucket
from .font import get_providers, item_references
from .pages import generate_pages

recipe_references: dict[Item, List[Recipe]] = {}


def _retrieve_recipes(bucket: Bucket) -> None:
    for recipe in bucket.get_all_recipes():
        result: Item = recipe.result

        if not result in recipe_references.keys():
            recipe_references[result] = []
        recipe_references[result].append(recipe)


def generate(ctx: TSContext, bucket: Bucket) -> None:
    _retrieve_recipes(bucket)
    font_data = get_providers(ctx, recipe_references)
    ctx.assets["tasty_supplies"].fonts["recipe_book"] = Font(font_data)

    pages = generate_pages(bucket, recipe_references, item_references)

    book_item = Item(
        "cookbook",
        base_item="written_book",
        max_stack_size=1,
        written_book_content={
            "title": "Tasty Supplies Cookbook",
            "author": "A Forgotten Chef",
            "resolved": False,
            "generation": 3,
            "pages": pages,
        },
        rarity=Rarity.EPIC,
        enchantment_glint_override=False,
    )

    bucket.add_item(book_item)
    bucket.add_recipe(
        ShapelessRecipe(
            [
                "minecraft:book",
                "minecraft:wheat",
            ],
            result=bucket.get("cookbook"),
        )
    )
