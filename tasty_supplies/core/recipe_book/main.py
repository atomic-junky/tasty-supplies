import json
from typing import List
from beet import Font

from ..models import TSContext, Item, Recipe
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
    font_data = get_providers(recipe_references)
    ctx.assets["tasty_supplies"].fonts["recipe_book"] = Font(font_data)

    pages = generate_pages(recipe_references, item_references)

    book_item = Item(
        "tasty_cookbook",
        base_item="written_book",
        max_stack_size=1,
        written_book_content={
            "title": "Tasty Cookbook",
            "author": "A Forgotten Chef",
            "resolved": False,
            "generation": 3,
            "pages": pages,
        },
    )

    bucket.add_item(book_item, category="recipe_book")
