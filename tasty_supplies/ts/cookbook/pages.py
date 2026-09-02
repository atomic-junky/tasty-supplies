"""Laying out the pages of the recipe book.

A page is a raw text component: a title, a grid glyph, then one glyph per
ingredient positioned with space glyphs whose width ``font.py`` measures.
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Union

from PIL import ImageFont

from ..item import Item
from ..recipe import (
    Brewing,
    Cut,
    RecipeSpec,
    Ref,
    Shaped,
    Shapeless,
    Smithing,
    ref_key,
    ref_title,
)
from ..registry import Registry
from ..translatable import Translatable
from .font import Glyphs

PAGE_WIDTH = 114
TITLE_MAX_LINES = 3

SUM_ITEMS_PER_LINE = 7
SUM_MAX_ITEM_PER_PAGES = 35

FONT_DIR = os.path.join(os.path.dirname(__file__), "../../src/assets/minecraft/font")
FONT_BOLD = ImageFont.truetype(os.path.join(FONT_DIR, "stwb.ttf"), size=9)
FONT_REGULAR = ImageFont.truetype(os.path.join(FONT_DIR, "stwb.ttf"), size=9)

BOOK_FONT = "tasty_supplies:recipe_book"

TOOLTIP_COMPONENTS = (
    "item_name",
    "rarity",
    "attribute_modifiers",
    "potion_contents",
    "max_damage",
)


@dataclass(frozen=True)
class GridConfig:
    cols: List[int]
    result_x: int
    result_row: int
    num_rows: int
    grid_key: str


GRID_BREWING = GridConfig(
    cols=[50], result_x=84, result_row=2, num_rows=3, grid_key="grid_brewing"
)
GRID_CRAFTING = GridConfig(
    cols=[14, 32, 50], result_x=84, result_row=1, num_rows=3, grid_key="grid_crafting"
)
GRID_COOKING = GridConfig(
    cols=[32], result_x=66, result_row=1, num_rows=2, grid_key="grid_cooking"
)
GRID_CUTTING = GridConfig(
    cols=[32], result_x=66, result_row=1, num_rows=2, grid_key="grid_cutting"
)
GRID_SMITHING = GridConfig(
    cols=[14, 32, 50], result_x=84, result_row=1, num_rows=2, grid_key="grid_smithing"
)

_SLOT_POS: Dict[str, tuple] = {
    f"{col}{row}": (row - 1, ord(col) - ord("A"))
    for row in range(1, 4)
    for col in "ABC"
}


def get_text_width(text: str, font: ImageFont.FreeTypeFont = FONT_REGULAR) -> int:
    return int(font.getlength(text)) if text else 0


def wrap_line(text: str, font: ImageFont.FreeTypeFont = FONT_REGULAR) -> List[str]:
    lines: List[str] = []
    current = ""
    for word in text.split():
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
    num_spaces = round((PAGE_WIDTH - text_width) / 2 / get_text_width(" ", font))
    return " " * num_spaces + line


def wrap_and_center(
    text: str, font: ImageFont.FreeTypeFont = FONT_REGULAR
) -> List[str]:
    return [center_line(line, font) for line in wrap_line(text, font)]


def _spaces(pixels: int) -> str:
    """Space glyphs adding up to the requested offset."""

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


def _arrange_shapeless(ingredients: list) -> Dict[str, Any]:
    """Lay shapeless ingredients out so they read like a crafting grid."""

    i = ingredients
    layouts = {
        1: ["B2"],
        2: ["A2", "B2"],
        3: ["A2", "B2", "B3"],
        4: ["A2", "B2", "A3", "B3"],
        5: ["A2", "B2", "C2", "A3", "B3"],
        6: ["A2", "B2", "C2", "A3", "B3", "C3"],
        7: ["A1", "B1", "C1", "A2", "B2", "C2", "B3"],
        8: ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3"],
        9: ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"],
    }
    return dict(zip(layouts[min(len(i), 9)], i))


def _slots_to_grid(slots: Dict[str, Any]) -> List[list]:
    grid: List[list] = [[None] * 3 for _ in range(3)]
    for slot_name, ingredient in slots.items():
        if ingredient is not None:
            row, col = _SLOT_POS[slot_name]
            grid[row][col] = ingredient
    return grid


def _build_grid(recipe: RecipeSpec) -> tuple:
    """The 3x3 matrix of ingredients, and which grid picture to draw."""

    if isinstance(recipe, Shaped):
        grid: List[list] = [[None] * 3 for _ in range(3)]
        for r, row in enumerate(recipe.pattern):
            for c, char in enumerate(row):
                if char in recipe.key:
                    grid[r][c] = recipe.key[char]
        return grid, GRID_CRAFTING

    if isinstance(recipe, Shapeless):
        return _slots_to_grid(_arrange_shapeless(recipe.items)), GRID_CRAFTING

    if isinstance(recipe, Smithing):
        grid: List[list] = [[None] * 3 for _ in range(3)]
        grid[1][0] = recipe.template
        grid[1][1] = recipe.base
        grid[1][2] = recipe.addition
        return grid, GRID_SMITHING

    if isinstance(recipe, Brewing):
        grid: List[list] = [[None] * 3 for _ in range(3)]
        grid[0][0] = recipe.reagent
        grid[2][0] = recipe.input
        return grid, GRID_BREWING

    grid = [[None] * 3 for _ in range(3)]
    ingredient = getattr(recipe, "ingredient", None)
    if ingredient:
        grid[1][0] = ingredient

    return grid, GRID_CUTTING if isinstance(recipe, Cut) else GRID_COOKING


def _drawable(ingredient: Ref, glyphs: Glyphs) -> tuple:
    """The glyph and the item behind a grid slot, or empty."""

    if not ingredient or isinstance(ingredient, dict):
        return "", ""
    return glyphs.char(ref_key(ingredient)), ingredient


def _item_component(
    text: str, ingredient: Union[Item, str], item_page_map: Dict[str, int]
) -> dict:
    """A glyph the reader can hover for a tooltip and click to jump to a page."""

    # A glyph is tinted by the text colour, and a book writes in dark ink.
    component: Dict[str, Any] = {"text": text, "color": "white"}

    if isinstance(ingredient, Item):
        component["hover_event"] = {
            "action": "show_item",
            "id": f"minecraft:{ingredient.support.id}",
            "count": 1,
        }
        shown = {
            key: value
            for key, value in ingredient.components.items()
            if key in TOOLTIP_COMPONENTS
        }
        if shown:
            component["hover_event"]["components"] = shown
    elif ingredient.startswith("#"):
        # A tag is drawn with one of its members, so say it takes any of them.
        component["hover_event"] = {
            "action": "show_text",
            "value": f"Any {ref_title(ingredient)}",
        }
    else:
        component["hover_event"] = {
            "action": "show_item",
            "id": ingredient if ":" in ingredient else f"minecraft:{ingredient}",
            "count": 1,
        }

    page = item_page_map.get(ref_key(ingredient))
    if page:
        component["click_event"] = {"action": "change_page", "page": page}

    return component


def _grid_row(
    row: int,
    grid: List[list],
    config: GridConfig,
    glyphs: Glyphs,
    item_page_map: Dict[str, int],
    result: Ref,
    result_char: str,
) -> List[dict]:
    components: List[dict] = []
    cursor_x = 0

    for column, target_x in enumerate(config.cols):
        char, ingredient = _drawable(grid[row][column], glyphs)
        if not char:
            continue

        components.append({"text": _spaces(target_x - cursor_x)})
        components.append(_item_component(char, ingredient, item_page_map))
        cursor_x = target_x + glyphs.advance(ref_key(ingredient))

    if row == config.result_row:
        components.append({"text": _spaces(config.result_x - cursor_x)})
        components.append(_item_component(result_char, result, item_page_map))

    return components


def _recipe_page(
    recipe: RecipeSpec,
    glyphs: Glyphs,
    index: int,
    total: int,
    item_page_map: Dict[str, int],
) -> dict:
    extra: List[dict] = []

    title = ref_title(recipe.result)
    if total > 1:
        title += f" ({index}/{total})"

    lines = wrap_and_center(title, FONT_BOLD)
    i = 0
    for line in lines:
        extra.append(Translatable(f"ts.cookbook.recipe.{recipe.id}.title.line.{i}", line + "\n", font="minecraft:stwb", color="black"))
        i+=1

    i = len(lines)
    for _ in range(TITLE_MAX_LINES - len(lines)):
        extra.append(Translatable(f"ts.cookbook.recipe.{recipe.id}.title.line.{i}", "\n", font="minecraft:stwb", color="black"))
        i+=1

    grid, config = _build_grid(recipe)
    extra.append({"text": glyphs.char(config.grid_key), "color": "white"})
    extra.append({"text": "\n\n\n"})  # Top margin

    result_char = glyphs.chars.get(ref_key(recipe.result), "<?>")
    for row in range(config.num_rows):
        extra += _grid_row(
            row, grid, config, glyphs, item_page_map, recipe.result, result_char
        )
        extra.append({"text": "\n\n"})

    return _page(extra)


def _cover_page() -> dict:
    extra: List[dict] = []

    title_lines = wrap_and_center("Tasty Supplies Cookbook", FONT_BOLD)
    title_lines += ["", ""] # Margin
    i = 0
    for line in title_lines:
        extra.append(
            Translatable(f"ts.cookbook.title.line.{i}", line + "\n", font="minecraft:stwb", color="gold")
        )
        i+=1

    desc_lines = wrap_and_center("Recipes & Guides", FONT_REGULAR)
    i = 0
    for line in desc_lines:
        extra.append(
            Translatable(f"ts.cookbook.desc.line.{i}", line + "\n", font="minecraft:stwr", color="dark_gray")
        )
        i+=1
    
    return _page(extra)


def _results_by_category(registry: Registry) -> Dict[str, List[str]]:
    """The results shown in the book, grouped by category, without repeats.

    Categories follow the order the catalog declares them in.
    """

    categories: Dict[str, List[str]] = {name: [] for name in registry.categories}

    for recipe in registry.recipes:
        if not recipe.book:
            continue
        results = categories.setdefault(recipe.ts_category, [])
        result = ref_key(recipe.result)
        if result not in results:
            results.append(result)

    return {name: results for name, results in categories.items() if results}


def _summary_pages(
    registry: Registry, glyphs: Glyphs, item_page_map: Dict[str, int]
) -> List[dict]:
    """One page per category, listing its items as clickable glyphs."""

    pages: List[dict] = []

    for category, results in _results_by_category(registry).items():
        for start in range(0, len(results), SUM_MAX_ITEM_PER_PAGES):
            extra: List[dict] = []
            i = 0
            for line in wrap_and_center(category.title(), FONT_BOLD):
                category_id = category.lower().replace(" ", "_")
                extra.append(Translatable(f"ts.cookbook.category.{category_id}.line.{i}", line + "\n", font="minecraft:stwb"))
                i += 1
            
            extra.append({"text": "\n\n\n"})  # Margin

            shown = results[start : start + SUM_MAX_ITEM_PER_PAGES]
            for position, result in enumerate(shown, start=1):
                target = item_page_map.get(result, 1)
                extra.append(
                    {
                        "text": glyphs.char(result),
                        "color": "white",
                        "click_event": {"action": "change_page", "page": target},
                        "hover_event": {
                            "action": "show_text",
                            "value": Translatable(f"ts.cookbook.action.change_page", "Go to page %s", with_args=[str(target)]),
                        },
                    }
                )
                if position % SUM_ITEMS_PER_LINE == 0:
                    extra.append({"text": "\n\n"})

            pages.append(_page(extra))

    return pages


def build(
    registry: Registry, groups: Dict[str, List[RecipeSpec]], glyphs: Glyphs
) -> List[dict]:
    """The whole book: cover, summary, then one page per recipe."""

    summary_page_count = sum(
        (len(results) - 1) // SUM_MAX_ITEM_PER_PAGES + 1
        for results in _results_by_category(registry).values()
    )

    page = 1 + summary_page_count + 1
    item_page_map: Dict[str, int] = {}
    for key, recipes in groups.items():
        item_page_map[key] = page
        page += len(recipes)

    pages = [_cover_page()]
    pages += _summary_pages(registry, glyphs, item_page_map)

    for recipes in groups.values():
        for index, recipe in enumerate(recipes, start=1):
            pages.append(
                _recipe_page(recipe, glyphs, index, total=len(recipes), item_page_map=item_page_map)
            )

    return pages


def _page(extra: List[dict]) -> dict:
    """A page. Its parts inherit the font and the colour from it."""

    return {"raw": {"text": "", "font": BOOK_FONT, "extra": extra}}
