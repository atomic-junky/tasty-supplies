from ts import Item, apply_effect, food, remainder, shapeless, stack


@food(1, 6, can_always_eat=True)
@stack(1)
@apply_effect("nausea", 300)
@apply_effect("fire_resistance", 6000)
@remainder("bucket")
@shapeless(
    "bucket",
    "magma_cream",
    "magma_cream",
    "magma_cream",
    "blaze_powder",
    "blaze_powder",
)
class MagmaGelatin(Item):
    pass
