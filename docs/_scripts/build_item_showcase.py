import glob
import math

from PIL import Image


UI_HEADER = Image.open("../_media/assets/ui_displayer_header.png", "r")
UI_SLOTS = Image.open("../_media/assets/ui_displayer_slots.png", "r")
UI_FOOTER = Image.open("../_media/assets/ui_displayer_footer.png", "r")
ITEMS_LOCATION = "../../tasty_supplies/src/assets/tasty_supplies/textures/item/*.png"

item_textures = []


def main():
    _load_item_textures()
    im = _build_displayer()
    im = _append_items(im)

    new_size = tuple(i * 3 for i in im.size)
    im = im.resize(new_size, Image.Resampling.NEAREST)

    im.save("../_media/showcase/item_showcase.png")


def _load_item_textures():
    paths = glob.glob(ITEMS_LOCATION)
    paths.sort()

    for path in paths:
        texture = Image.open(path)
        item_textures.append(texture)


def _build_displayer():
    col = 9
    raw = math.ceil(len(item_textures) / col)

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

    for texture in item_textures:
        index = item_textures.index(texture)
        raw = math.floor(index / 9)
        col = index - raw * 9

        mask = _create_a_mask(texture)

        im.paste(
            texture,
            (
                padding[0] + col * (16 + 1) + col + 1,
                padding[1] + raw * (16 + 1) + raw + 1,
            ),
            mask,
        )

    return im


def _create_a_mask(im: Image):
    return im.convert("LA")


if __name__ == "__main__":
    main()
