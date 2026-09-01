from ts import Item, food, shapeless


@food(3, 0.5)
@shapeless(
    "melon_slice", "melon_slice", "melon_slice", "melon_slice", "ice", "ice", "stick"
)
class MelonPopsicle(Item):
    pass
