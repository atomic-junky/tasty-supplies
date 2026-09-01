"""The font backing the recipe book.

Every item drawn in the book is a glyph of a dedicated font, and the layout is
made of negative and positive spaces. The glyph table is built per build and
passed around.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, Iterator, List

from beet import Context

from ..recipe import RecipeSpec, Ref, ref_key
from .textures import Textures

logger = logging.getLogger(__name__)

#: Fallback advance, in pixels, when a texture cannot be measured.
DEFAULT_ADVANCE = 17

GRIDS = {
    "grid_cooking": chr(0xE901),
    "grid_crafting": chr(0xE902),
    "grid_cutting": chr(0xE903),
    "grid_smithing": chr(0xE904),
}


@dataclass
class Glyphs:
    """Which character draws an item, and how wide it is."""

    chars: Dict[str, str] = field(default_factory=dict)
    advances: Dict[str, int] = field(default_factory=dict)

    def char(self, name: str) -> str:
        return self.chars.get(name, "")

    def advance(self, name: str) -> int:
        return self.advances.get(name, DEFAULT_ADVANCE)


def build(ctx: Context, groups: Dict[str, List[RecipeSpec]], glyphs: Glyphs) -> dict:
    """Build the font providers, filling in the glyph table along the way."""

    textures = Textures(ctx)

    wanted: Dict[str, str] = {}
    for ref in _drawn(groups):
        name = ref_key(ref)
        if name in wanted:
            continue
        texture = textures.of(ref)
        if texture is None:
            logger.warning("Nothing to draw for %r in the recipe book.", name)
            continue
        wanted[name] = texture

    textures.render_pending()

    providers: List[dict] = [_spaces()]
    providers += [_grid(name, char) for name, char in GRIDS.items()]
    glyphs.chars.update(GRIDS)

    for name, texture in wanted.items():
        if not textures.exists(texture):
            logger.warning("Missing texture %r for the recipe book.", texture)
            continue

        char = chr(0xE000 + len(glyphs.chars) - len(GRIDS))
        providers.append(
            {
                "type": "bitmap",
                "file": texture,
                "height": 16,
                "ascent": 16,
                "chars": [char],
            }
        )
        glyphs.chars[name] = char
        glyphs.advances[name] = _advance(textures, texture)

    return {"providers": providers}


def _drawn(groups: Dict[str, List[RecipeSpec]]) -> Iterator[Ref]:
    """Every result and ingredient the book draws, results first."""

    for recipes in groups.values():
        yield recipes[0].result

    for recipes in groups.values():
        for recipe in recipes:
            yield from recipe.ingredients()


def _spaces() -> dict:
    """Negative and positive spacing, one glyph per pixel offset."""

    advances = {}
    for pixels in range(1, 101):
        advances[chr(0xF000 + pixels)] = -pixels
        advances[chr(0xF100 + pixels)] = pixels
    return {"type": "space", "advances": advances}


def _grid(name: str, char: str) -> dict:
    return {
        "type": "bitmap",
        "file": f"tasty_supplies:recipe_book/{name}.png",
        "height": 74,
        "ascent": 0,
        "chars": [char],
    }


def _advance(textures: Textures, texture: str) -> int:
    """Width of a texture glyph, in pixels.

    Minecraft keeps the empty space on the left of a texture but crops it on
    the right, and adds exactly one pixel of spacing: the advance is therefore
    the rightmost non-empty pixel plus one.
    """

    image = textures.image(texture)
    if image is None:
        return DEFAULT_ADVANCE

    box = image.convert("RGBA").split()[-1].getbbox()
    return box[2] + 1 if box else DEFAULT_ADVANCE
