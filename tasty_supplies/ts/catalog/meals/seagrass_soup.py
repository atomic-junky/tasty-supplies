from ts import Item, food, remainder, shapeless


@food(4, 3.6)
@remainder("bowl")
@shapeless("bowl", "seagrass", "seagrass", "#tasty_supplies:water")
class SeagrassSoup(Item):
    pass
