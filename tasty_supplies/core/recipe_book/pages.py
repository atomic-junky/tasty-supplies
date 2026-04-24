import os
from dataclasses import dataclass
from typing import Union

from ..models import (
    Item,
    ShapedRecipe,
    ShapelessRecipe,
    CuttingBoardRecipe,
)
from PIL import ImageFont

PAGE_WIDTH = 114
TITLE_MAX_LINES = 3

FONT_BOLD = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), "../../src/assets/minecraft/font/stwb.ttf"),
    size=9,
)
FONT_REGULAR = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), "../../src/assets/minecraft/font/stwb.ttf"),
    size=9,
)


@dataclass(frozen=True)
class GridConfig:
    cols: list[int]
    result_x: int
    result_row: int
    num_rows: int
    grid_key: str


GRID_CRAFTING = GridConfig(
    cols=[14, 32, 50], result_x=84, result_row=1, num_rows=3, grid_key="grid_crafting"
)
GRID_COOKING = GridConfig(
    cols=[32], result_x=66, result_row=1, num_rows=2, grid_key="grid_cooking"
)
GRID_CUTTING = GridConfig(
    cols=[32], result_x=66, result_row=1, num_rows=2, grid_key="grid_cutting"
)

_SLOT_POS: dict[str, tuple[int, int]] = {
    f"{col}{row}": (row - 1, ord(col) - ord("A"))
    for row in range(1, 4)
    for col in "ABC"
}


def get_text_width(text: str, font: ImageFont.FreeTypeFont = FONT_REGULAR) -> int:
    return int(font.getlength(text)) if text else 0


def wrap_line(text: str, font: ImageFont.FreeTypeFont = FONT_REGULAR) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if get_text_width(candidate, font) <= PAGE_WIDTH:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def center_line(line: str, font: ImageFont.FreeTypeFont = FONT_REGULAR) -> str:
    line = line.strip()
    text_width = get_text_width(line, font)
    if text_width >= PAGE_WIDTH:
        return line
    space_width = get_text_width(" ", font)
    num_spaces = round((PAGE_WIDTH - text_width) / 2 / space_width)
    return " " * num_spaces + line


def wrap_and_center(
    text: str, font: ImageFont.FreeTypeFont = FONT_REGULAR
) -> list[str]:
    return [center_line(line, font) for line in wrap_line(text, font)]


def _get_spaces(pixels: int) -> str:
    result = ""
    while pixels > 100:
        result += chr(0xF100 + 100)
        pixels -= 100
    while pixels < -100:
        result += chr(0xF000 + 100)
        pixels += 100
    if pixels > 0:
        result += chr(0xF100 + pixels)
    elif pixels < 0:
        result += chr(0xF000 + abs(pixels))
    return result


def _arrange_shapeless(ingredients: list) -> dict[str, object]:
    n = len(ingredients)
    i = ingredients

    if n == 1:
        return {"B2": i[0]}
    if n == 2:
        return {"A2": i[0], "B2": i[1]}
    if n == 3:
        return {"A2": i[0], "B2": i[1], "B3": i[2]}
    if n == 4:
        return {"A2": i[0], "B2": i[1], "A3": i[2], "B3": i[3]}
    if n == 5:
        return {"A2": i[0], "B2": i[1], "C2": i[2], "A3": i[3], "B3": i[4]}
    if n == 6:
        return {"A2": i[0], "B2": i[1], "C2": i[2], "A3": i[3], "B3": i[4], "C3": i[5]}
    if n == 7:
        return {
            "A1": i[0],
            "B1": i[1],
            "C1": i[2],
            "A2": i[3],
            "B2": i[4],
            "C2": i[5],
            "B3": i[6],
        }
    if n == 8:
        return {
            "A1": i[0],
            "B1": i[1],
            "C1": i[2],
            "A2": i[3],
            "B2": i[4],
            "C2": i[5],
            "A3": i[6],
            "B3": i[7],
        }
    # n == 9
    slots = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
    return dict(zip(slots, i))


def _slots_to_grid(slots: dict[str, object]) -> list[list]:
    grid = [[None] * 3 for _ in range(3)]
    for slot_name, ingredient in slots.items():
        if ingredient is not None:
            row, col = _SLOT_POS[slot_name]
            grid[row][col] = ingredient
    return grid


def _build_grid_matrix(recipe) -> tuple[list[list], GridConfig]:
    if isinstance(recipe, ShapedRecipe):
        grid = [[None] * 3 for _ in range(3)]
        for r, row in enumerate(recipe.pattern):
            for c, char in enumerate(row):
                if char in recipe.key:
                    grid[r][c] = recipe.key[char]
        return grid, GRID_CRAFTING

    if isinstance(recipe, ShapelessRecipe):
        slots = _arrange_shapeless(recipe.ingredients)
        return _slots_to_grid(slots), GRID_CRAFTING

    ingredient = None
    if hasattr(recipe, "ingredient"):
        ingredient = recipe.ingredient

    # TODO: Support SmithingTransformRecipe which has two ingredients.

    grid = [[None] * 3 for _ in range(3)]
    if ingredient:
        grid[1][0] = ingredient

    if isinstance(recipe, CuttingBoardRecipe):
        return grid, GRID_CUTTING

    return grid, GRID_COOKING


def _resolve_ingredient(
    ingredient, item_references: dict[str, str]
) -> tuple[str, Union[Item, str]]:
    """Returns (display_char, item) or ("", "") if empty."""
    if not ingredient:
        return "", ""
    if isinstance(ingredient, Item):
        return (
            item_references.get(ingredient.name, ""),
            ingredient,
        )
    if isinstance(ingredient, str) and not ingredient.startswith("#"):
        return (
            item_references.get(ingredient.removeprefix("minecraft:"), ""),
            ingredient,
        )
    if isinstance(ingredient, dict) and "item" in ingredient:
        raw = ingredient["item"]
        return item_references.get(raw.removeprefix("minecraft:"), ""), raw
    return "", ""


def _make_item_component(
    text: str, item: Union[Item, str], item_page_map: dict[str, int]
) -> dict:
    comp = {
        "text": text,
        "font": "tasty_supplies:recipe_book",
        "color": "white",
    }

    if isinstance(item, Item):
        comp["hover_event"] = {
            "action": "show_item",
            "id": f"minecraft:{item.base_item.removeprefix('minecraft:')}",
            "count": 1,
        }
        if item.components:
            comp["hover_event"]["components"] = item.components
        clean_id = item.name
    else:
        comp["hover_event"] = {
            "action": "show_item",
            "id": item if ":" in item else f"minecraft:{item}",
            "count": 1,
        }
        clean_id = item.removeprefix("minecraft:")

    if clean_id in item_page_map:
        comp["click_event"] = {
            "action": "change_page",
            "page": item_page_map[clean_id],
        }
    return comp


def _build_grid_row(
    r: int,
    grid: list[list],
    config: GridConfig,
    item_references: dict[str, str],
    item_page_map: dict[str, int],
    result_item: Item,
    result_char: str,
    grid_char: str,
) -> list[dict]:
    from .font import item_advances

    components: list[dict] = []
    cursor_x = 0

    for c, target_x in enumerate(iterable=config.cols):
        char, item_id = _resolve_ingredient(grid[r][c], item_references)
        if not char:
            continue

        name = (
            item_id.name
            if isinstance(item_id, Item)
            else item_id.removeprefix("minecraft:")
        )
        advance = item_advances.get(name, 17)

        components.append(
            {
                "text": _get_spaces(target_x - cursor_x),
                "font": "tasty_supplies:recipe_book",
            }
        )
        components.append(_make_item_component(char, item_id, item_page_map))
        cursor_x = target_x + advance

    if r == config.result_row:
        name = result_item.name
        advance = item_advances.get(name, 17)

        components.append(
            {
                "text": _get_spaces(config.result_x - cursor_x),
                "font": "tasty_supplies:recipe_book",
            }
        )
        components.append(_make_item_component(result_char, result_item, item_page_map))

    return components


def _generate_page(
    recipe,
    item_references: dict[str, str],
    recipe_index: int = 1,
    total_recipes: int = 1,
    item_page_map: dict[str, int] | None = None,
) -> dict:
    if item_page_map is None:
        item_page_map = {}

    text_components: list[dict] = []

    display_title = recipe.result.name.replace("_", " ").title()
    if total_recipes > 1:
        display_title += f" ({recipe_index}/{total_recipes})"

    title_lines = wrap_and_center(display_title, FONT_BOLD)
    for line in title_lines:
        text_components.append({"text": line + "\\n", "font": "minecraft:stwb"})
    for _ in range(TITLE_MAX_LINES - len(title_lines)):
        text_components.append({"text": "\\n"})

    grid, config = _build_grid_matrix(recipe)
    grid_char = item_references.get(config.grid_key, "")
    result_char = item_references.get(recipe.result.name, "<?>")

    text_components.append(
        {"text": grid_char, "font": "tasty_supplies:recipe_book", "color": "white"}
    )
    text_components.append({"text": "\\n\\n\\n"})  # Margin top

    for r in range(config.num_rows):
        row_comps = _build_grid_row(
            r,
            grid,
            config,
            item_references,
            item_page_map,
            recipe.result,
            result_char,
            grid_char,
        )
        text_components.extend(row_comps)
        text_components.append({"text": "\\n\\n"})

    return {"raw": {"text": "", "extra": text_components}}


def generate_pages(
    recipe_references: dict[Item, list],
    item_references: dict[str, str],
) -> list[dict]:
    item_page_map: dict[str, int] = {}
    current_page = 1
    for recipes in recipe_references.values():
        if recipes and recipes[0].result and hasattr(recipes[0].result, "name"):
            item_page_map[recipes[0].result.name] = current_page
        current_page += len(recipes)

    return [
        _generate_page(recipe, item_references, i + 1, len(recipes), item_page_map)
        for recipes in recipe_references.values()
        for i, recipe in enumerate(recipes)
    ]
