"""The font backing the recipe book.

Every item drawn in the book is a glyph of a dedicated font, and the layout is
made of negative and positive spaces. The glyph table is built per build and
passed around.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from beet import Context, ResourcePack
from beet.contrib.vanilla import Vanilla

from ..recipe import RecipeSpec, Ref, ref_key, ref_texture

#: Fallback advance, in pixels, when a texture cannot be measured.
DEFAULT_ADVANCE = 17

GRIDS = {
    "grid_cooking": chr(0xE901),
    "grid_crafting": chr(0xE902),
    "grid_cutting": chr(0xE903),
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

    vanilla = ctx.inject(Vanilla).assets

    providers: List[dict] = [_spaces()]
    providers += [_grid(name, char) for name, char in GRIDS.items()]
    glyphs.chars.update(GRIDS)

    codepoint = 0

    def add(ref: Ref) -> None:
        nonlocal codepoint

        if isinstance(ref, dict) or (isinstance(ref, str) and ref.startswith("#")):
            return

        name = ref_key(ref)
        texture = ref_texture(ref)
        if texture and texture.startswith("minecraft:"):
            # TODO: support ingredients drawn with a non-item texture.
            if vanilla.textures.get(texture.removesuffix(".png")) is None:
                texture = None

        if name not in glyphs.advances:
            glyphs.advances[name] = _advance(ctx, vanilla, texture)

        if texture and name not in glyphs.chars:
            char = chr(0xE000 + codepoint)
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
            codepoint += 1

    for recipes in groups.values():
        add(recipes[0].result)

    for recipes in groups.values():
        for recipe in recipes:
            for ingredient in recipe.ingredients():
                add(ingredient)

    return {"providers": providers}


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


def _advance(ctx: Context, vanilla: ResourcePack, texture: Optional[str]) -> int:
    """Width of a texture glyph, in pixels.

    Minecraft keeps the empty space on the left of a texture but crops it on
    the right, and adds exactly one pixel of spacing: the advance is therefore
    the rightmost non-empty pixel plus one.
    """

    if not texture:
        return DEFAULT_ADVANCE

    path = texture.removesuffix(".png")
    pack = vanilla if path.startswith("minecraft:") else ctx.assets
    image = pack.textures.get(path)

    if image is None or not getattr(image, "image", None):
        return DEFAULT_ADVANCE

    box = image.image.convert("RGBA").split()[-1].getbbox()
    return box[2] + 1 if box else DEFAULT_ADVANCE
