from ts import Item, apply_effect, food, remainder, shapeless


@food(5, 6)
@remainder("bowl")
@apply_effect("nausea", 600)
@shapeless("bowl", "crimson_fungus", "warped_fungus")
class NetherSalad(Item):
    pass
