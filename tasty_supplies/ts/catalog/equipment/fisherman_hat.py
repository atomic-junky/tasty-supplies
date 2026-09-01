from ts import shaped

from ._equippable import Equippable


@shaped([" W ", "WFW"], W="leather", F="cod")
class FishermanHat(Equippable):
    pass
