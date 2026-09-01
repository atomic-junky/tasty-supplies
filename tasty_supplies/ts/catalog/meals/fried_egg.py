from ts import Item, bases, cooked, food


@food(8, 2.4)
@cooked("#minecraft:eggs", time=140, xp=0.1)
class FriedEgg(Item):
    base = bases.FRIED_EGG
