from ts import Item, food, shapeless

from ..ingredients.butter import Butter


@food(8, 12.8)
@shapeless("wheat", "sugar", "#minecraft:eggs", Butter)
class SweetRoll(Item):
    pass
