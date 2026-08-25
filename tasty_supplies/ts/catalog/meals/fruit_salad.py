from ts import Item, apply_effect, food, remainder, shapeless


@food(18, 7.6)
@remainder("bowl")
@apply_effect("regeneration", 600)
@shapeless(
    "bowl",
    "apple",
    "apple",
    "melon_slice",
    "melon_slice",
    "#tasty_supplies:berries",
    "#tasty_supplies:berries",
)
class FruitSalad(Item):
    pass
