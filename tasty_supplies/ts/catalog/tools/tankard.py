from typing import List

from ts import bases, Item, shaped, stack


@shaped(count=3, pattern=["mm ", "mms", "mm "], key={"m": "#minecraft:planks", "s": "stick"})
class Tankard(Item):
    base = bases.TANKARD