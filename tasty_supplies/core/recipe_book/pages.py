import json
from base64 import b64encode
from ..models import Item, Recipe


def _get_space(pixels: int) -> str:
    """Returns a JSON text component string for spacing."""
    if pixels == 0:
        return ""
    if pixels < 0:
        # Map to \uF0XX for negative
        return chr(0xF000 + abs(pixels))
    else:
        # Map to \uF1XX for positive
        return chr(0xF100 + pixels)


def _generate_page(recipe: Recipe, item_references: dict[str, str]) -> list[dict]:
    """Generates the JSON text for a single book page for a recipe."""
    text_components = []

    # Title
    result_item: Item = recipe.result
    # result_item.name should be converted nicely
    display_title = result_item.name.replace("_", " ").title()
    title = f"{display_title}\\n\\n"
    text_components.append({"text": title, "font": "minecraft:default", "bold": True})

    # Grid character
    is_3x3 = len(getattr(recipe, "pattern", [])) > 2
    grid_char = (
        item_references.get("grid_3x3") if is_3x3 else item_references.get("grid_2x2")
    )
    if not grid_char:
        # Fallback if grid texture is somehow missing
        grid_char = ""

    text_components.append({"text": grid_char, "font": "tasty_supplies:recipe_book"})

    # Render basic placeholder spaces for ingredients overlapping the grid
    # This is an approximation. In a typical grid layout, we would place each ingredient character,
    # then go backward (-18 or -54 pixels depending on layer) to draw the next.

    # Draw result item
    result_char = item_references.get(result_item.name, "?")

    # 54 pixels back horizontally (approx for right side alignment, needs manual adjustment later)
    # text_components.append({"text": _get_space(-54), "font": "tasty_supplies:recipe_book"})

    text_components.append(
        {
            "text": f"{_get_space(-18)}{result_char}",
            "font": "tasty_supplies:recipe_book",
        }
    )

    return text_components


def generate_pages(
    recipe_references: dict[Item, list[Recipe]], item_references: dict[str, str]
) -> list[str]:
    """Generates a list of all raw JSON text strings for the book pages."""
    pages = []

    for recipes in recipe_references.values():
        for recipe in recipes:
            page_json = _generate_page(recipe, item_references)
            pages.append(page_json)

    return pages
