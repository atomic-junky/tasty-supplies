from ts import Item, apply_effect, food, remainder, shapeless


@food(6, 11)
@remainder("bowl")
@apply_effect("nausea", 300)
@shapeless("warped_roots", "warped_roots", "bowl", "cooked_mutton")
class WarpedMutton(Item):
    pass
