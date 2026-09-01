from ts import Item, bases, component, shaped


@component(
    entity_data={
        "id": "minecraft:armor_stand",
        "Tags": ["cutting_board_placer"],
        "Invisible": True,
        "Small": True,
    }
)
@shaped(["spp", "spp"], p="#minecraft:planks", s="stick")
class CuttingBoard(Item):
    base = bases.ARMOR_STAND
    texture = "tasty_supplies:block/cutting_board"
    # TODO replace the item texture with the 2d texture present in tasty_supplies:item/
