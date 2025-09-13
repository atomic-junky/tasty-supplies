import math
import os

from beet import Context
from beet.contrib.vanilla import Vanilla
from PIL import Image


UI_HEADER = Image.open("./docs/_media/assets/ui_displayer_header.png", "r")
UI_SLOTS = Image.open("./docs/_media/assets/ui_displayer_slots.png", "r")
UI_FOOTER = Image.open("./docs/_media/assets/ui_displayer_footer.png", "r")
ITEM_LOCATION = "./tasty_supplies/src/assets/tasty_supplies/textures/item/"
BLOCK_LOCATION = "./tasty_supplies/src/assets/tasty_supplies/textures/block/"

item_textures = []


class TSContext(Context):
    def __init__(self, ctx: Context):
        self.__dict__ = ctx.__dict__.copy()
        self.vanilla = ctx.inject(Vanilla)
        self.showcase_items = []

    def _create_item_showcase(self):
        _load_item_textures(self.showcase_items)
        im = _build_displayer()
        im = _append_items(im)

        new_size = tuple(i * 3 for i in im.size)
        im = im.resize(new_size, Image.Resampling.NEAREST)

        im.save("./docs/_media/showcase/item_showcase.png")


def _load_item_textures(items: tuple):
    for item_name in items:
        if item_name == "\n":
            item_textures.append(item_name)
            continue
        elif f"{item_name}.png" in os.listdir(ITEM_LOCATION):
            path = os.path.join(ITEM_LOCATION, f"{item_name}.png")
        elif f"{item_name}.png" in os.listdir(BLOCK_LOCATION):
            path = os.path.join(BLOCK_LOCATION, f"{item_name}.png")

        item_textures.append(Image.open(path))


def _build_displayer():
    col = 0
    raw = 0
    idx = 0
    for item in item_textures:
        if isinstance(item, str):
            if idx >= len(item_textures) - 1:
                continue

            if col < 9:
                raw += 1

            col = 0
            raw += 1
            idx += 1
            continue
        col += 1
        if col >= 9:
            col = 0
            raw += 1
        idx += 1

    header_size = UI_HEADER.size
    slots_size = UI_SLOTS.size
    footer_size = UI_FOOTER.size

    im_height = header_size[1] + (slots_size[1] * raw) + footer_size[1]
    im = Image.new("RGBA", (header_size[0], im_height), (0, 0, 0))

    Image.Image.paste(im, UI_HEADER, (0, 0))

    for r in range(raw):
        Image.Image.paste(im, UI_SLOTS, (0, header_size[1] + slots_size[1] * r))

    Image.Image.paste(im, UI_FOOTER, (0, im_height - footer_size[1]))

    return im


def _append_items(im):
    padding = (7, UI_HEADER.size[1])

    raw = 0
    col = 0
    for texture in item_textures:
        if isinstance(texture, str):
            if col > 0:
                raw += 1
            raw += 1
            col = 0
            continue

        mask = _create_a_mask(texture)

        im.paste(
            texture,
            (
                padding[0] + col * (16 + 1) + col + 1,
                padding[1] + raw * (16 + 1) + raw + 1,
            ),
            mask,
        )
        col += 1

        if col >= 9:
            col = 0
            raw += 1

    return im


def _create_a_mask(im: Image):
    return im.convert("LA")
