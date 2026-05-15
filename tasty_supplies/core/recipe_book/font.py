import os
from typing import List
from beet import ResourcePack, Texture

from ..models import Item, Recipe, TSContext

item_references: dict[str, str] = {}
item_advances: dict[str, int] = {}


def _get_char(char_idx: int) -> str:
    # Use proper unicode escape for json serialization
    return chr(0xE000 + char_idx)


def _get_texture_advance(ctx: TSContext, texture_path: str) -> int:
    """Calculate the pixel advance of a Minecraft texture font character.
    Minecraft does not crop empty space on the left, but it crops empty space
    on the right and forces exactly 1 pixel of spacing.
    Thus, the advance is the rightmost pixel's x-coordinate + 1.
    """
    if not texture_path:
        return 17

    is_vanilla = texture_path.startswith("minecraft:")
    tex_path_no_ext = texture_path.removesuffix(".png")
    if is_vanilla:
        tex = ctx.vanilla.assets.textures.get(tex_path_no_ext)
    else:
        tex = ctx.assets.textures.get(tex_path_no_ext)

    advance = 17
    if tex and hasattr(tex, "image") and tex.image:
        try:
            alpha = tex.image.convert("RGBA").split()[-1]
            bbox = alpha.getbbox()
            if bbox:
                # bbox[2] is the rightmost bounding box edge
                advance = bbox[2] + 1
        except Exception:
            pass

    return advance


def get_providers(
    ctx: TSContext, recipe_references: dict[Item, List[Recipe]]
) -> List[dict]:
    providers: List[dict] = []
    char_idx: int = 0
    space_advances = {}

    for i in range(1, 101):
        space_advances[chr(0xF000 + i)] = -i
        space_advances[chr(0xF100 + i)] = i

    providers.append({"type": "space", "advances": space_advances})

    # Grids
    providers.append(_register_grid("grid_cooking", chr(0xE901)))
    providers.append(_register_grid("grid_crafting", chr(0xE902)))
    providers.append(_register_grid("grid_cutting", chr(0xE903)))

    # Result textures
    for item in recipe_references.keys():
        if item.name not in item_references:
            texture_path = f"{item.texture_path}.png"
            provider: dict = {
                "type": "bitmap",
                "file": texture_path,
                "height": 16,
                "ascent": 16,
                "chars": [_get_char(char_idx)],
            }
            providers.append(provider)
            item_references[item.name] = _get_char(char_idx)

            item_advances[item.name] = _get_texture_advance(ctx, texture_path)

            char_idx += 1

    vanilla_assets: ResourcePack = ctx.vanilla.assets

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
        if hasattr(recipe, "key") and recipe.key:
            ing_items.extend(recipe.key.values())

        for ing in ing_items:
            # ing can be a string (vanilla), an Item (custom) or a dict.
            item_name = None
            texture_path = None

            if isinstance(ing, Item):
                item_name = ing.name
                texture_path = ing.texture_path + ".png"
            elif isinstance(ing, str) and not ing.startswith("#"):
                # Vanilla item
                item_name = ing.removeprefix("minecraft:")
                if vanilla_assets.textures.get(f"minecraft:item/{item_name}"):
                    texture_path = f"minecraft:item/{item_name}.png"

                # TODO support non-item textures

            if item_name and item_name not in item_advances:
                item_advances[item_name] = _get_texture_advance(ctx, texture_path)

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


def _register_grid(grid_name: str, char: str) -> dict:
    item_references[grid_name] = char

    provider = {
        "type": "bitmap",
        "file": f"tasty_supplies:recipe_book/{grid_name}.png",
        "height": 74,
        "ascent": 0,
        "chars": [char],
    }
    return provider
