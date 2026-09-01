from ts import Item, bases, cooked, cut, food

from .wheat_dough import WheatDough


@food(1, 0.4)
@cut(WheatDough, count=2)
class RawPasta(Item):
    base = bases.RAW_PASTA


@food(2, 1.4)
@cooked(RawPasta, time=100, xp=0.1)
class Pasta(Item):
    base = bases.PASTA
