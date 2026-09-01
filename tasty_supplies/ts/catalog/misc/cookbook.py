from ts import Item, bases, component, rarity, shaped, stack


@stack(1)
@rarity("epic")
@component(enchantment_glint_override=False)
@component(
    written_book_content={
        "title": "Tasty Supplies Cookbook",
        "author": "Mithaecus",
        "resolved": False,
        "generation": 3,
        "pages": [],
    }
)
@shaped(["WWW", "WBW", "WWW"], {"W": "minecraft:wheat", "B": "minecraft:book"})
class Cookbook(Item):
    base = bases.WRITTEN_BOOK
    book = False
