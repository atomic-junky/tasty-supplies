from ts import shaped

from ._equippable import Equippable


@shaped([" W ", "WWW"], W="wheat")
class FarmerHat(Equippable):
    pass
