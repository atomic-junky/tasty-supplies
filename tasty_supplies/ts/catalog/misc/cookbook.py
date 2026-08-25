from ts import Item, bases, component, rarity, shapeless, stack


@stack(1)
@rarity("epic")
@component(enchantment_glint_override=False)
@component(
    written_book_content={
        "title": "Tasty Supplies Cookbook",
        "author": "A Forgotten Chef",
        "resolved": False,
        "generation": 3,
        "pages": [],
    }
)
@shapeless("book", "wheat")
class Cookbook(Item):
    base = bases.WRITTEN_BOOK
    # Pages are laid out by the cookbook plugin, and the book skips its own.
    book = False
