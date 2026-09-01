from ts import Item, food, shaped

from ..ingredients.butter import Butter


@food(6, 3.4)
@shaped(["WBS", "WBS"], W="wheat", B=Butter, S="sugar")
class Croissant(Item):
    pass
