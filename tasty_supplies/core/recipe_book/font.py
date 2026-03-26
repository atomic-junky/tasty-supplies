import json
import os
from typing import List, Dict

from ..models import Item, Recipe

item_references: dict[str, str] = {}


def _get_char(char_idx: int) -> str:
    # Use proper unicode escape for json serialization
    return chr(0xE000 + char_idx)


def get_providers(recipe_references: dict[Item, List[Recipe]]) -> List[dict]:
    providers: List[dict] = []
    char_idx: int = 0

    # Add a space provider for precise positioning
    # We will use this to generate negative and positive spaces from -100 to 100
    space_advances = {}

    # We'll map characters \uF000 to \uF0C8 for negative spaces (-200 to 0)
    # and \uF100 to \uF1C8 for positive spaces (0 to 200)
    for i in range(1, 101):
        space_advances[chr(0xF000 + i)] = -i
        space_advances[chr(0xF100 + i)] = i

    providers.append({"type": "space", "advances": space_advances})

    # Grids
    providers.append(
        {
            "type": "bitmap",
            "file": "tasty_supplies:recipe_book/grid_2x2",
            "height": 55,
            "ascent": 34,
            "chars": [chr(0xE902)],
        }
    )
    item_references["grid_2x2"] = chr(0xE902)

    providers.append(
        {
            "type": "bitmap",
            "file": "tasty_supplies:recipe_book/grid_3x3",
            "height": 55,
            "ascent": 34,
            "chars": [chr(0xE903)],
        }
    )
    item_references["grid_3x3"] = chr(0xE903)

    # Result textures
    for item in recipe_references.keys():
        if item.name not in item_references:
            provider: dict = {
                "type": "bitmap",
                "file": item.texture_path,
                "height": 16,
                "ascent": 16,
                "chars": [_get_char(char_idx)],
            }
            providers.append(provider)
            item_references[item.name] = _get_char(char_idx)
            char_idx += 1

    # Ingredient textures
    recipes: list[Recipe] = [
        r for sublist in recipe_references.values() for r in sublist
    ]
    for recipe in recipes:
        ing_items = []
        if hasattr(recipe, "ingredient") and recipe.ingredient:
            ing_items.append(recipe.ingredient)
        if hasattr(recipe, "ingredients") and recipe.ingredients:
            if isinstance(recipe.ingredients, list):
                ing_items.extend(recipe.ingredients)
            elif isinstance(recipe.ingredients, dict):
                ing_items.extend(recipe.ingredients.values())

        for ing in ing_items:
            # ing can be a string (vanilla), an Item (custom) or a dict.
            item_name = None
            texture_path = None

            if isinstance(ing, Item):
                item_name = ing.name
                texture_path = ing.texture_path + ".png"
            elif isinstance(ing, str) and ing.startswith("minecraft:"):
                # Vanilla item
                item_name = ing.replace("minecraft:", "")
                # Default vanilla texture path
                texture_path = f"minecraft:item/{item_name}"
                # Some vanilla items are blocks, but item/ folder often works, or we can use a hardcoded list if needed.
                # For now let's use item/

            if item_name and texture_path and item_name not in item_references:
                provider = {
                    "type": "bitmap",
                    "file": texture_path,
                    "height": 16,
                    "ascent": 16,
                    "chars": [_get_char(char_idx)],
                }
                providers.append(provider)
                item_references[item_name] = _get_char(char_idx)
                char_idx += 1

    return {"providers": providers}
