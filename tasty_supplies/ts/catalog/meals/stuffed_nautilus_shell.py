from ts import Item, food, remainder, shapeless


@food(12, 16.4)
@remainder("nautilus_shell")
@shapeless("nautilus_shell", "carrot", "kelp", "baked_potato")
class StuffedNautilusShell(Item):
    pass
