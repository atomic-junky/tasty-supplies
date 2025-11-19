from typing import Any

from core.constants import MODEL_TYPE_ITEM, TASTY_SUPPLIES_NAMESPACE
from .. import (
    Item,
    ShapedRecipe,
    Category,
    Bucket,
)


class EquipementItem(Item):
    def __init__(self, item_name: str, slot: str, texture_name: str, **components: Any):
        self.slot = slot
        
        super().__init__(
            item_name=item_name,
            base_item=self._get_base_item(),
            max_stack_size=1,
            equippable={
                "slot": slot,
                "dispensable": True,
                "swappable": True
            },
            item_model=f"{TASTY_SUPPLIES_NAMESPACE}:{item_name}",
            **components
        )
    
    def _get_base_item(self) -> str:
        match self.slot:
            case "head":
                return "leather_helmet"
            case "chest":
                return "leather_chestplate"
            case "legs":
                return "leather_leggings"
            case "feet":
                return "leather_boots"


class Equipements(Category):
    """Category for equipements items."""

    def __init__(self, bucket: Bucket):
        """Initialize Equipements category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Equipements", bucket)

    def create_items(self):
        """Create all equipement items and add them to the bucket."""
        self.add_item(
            EquipementItem("farmer_hat", slot="head", texture_name="farmer")
        )
        
        self.add_item(
            EquipementItem("fisherman_hat", slot="head", texture_name="fisherman")
        )

    def create_recipes(self):
        """Create all equipement recipes."""
        self.add_recipe(
            ShapedRecipe(
                result=self.bucket.get("farmer_hat"),
                pattern=[
                    " W ",
                    "W W",
                ],
                key={
                    "W": "minecraft:wheat",
                },
            )
        )

        self.add_recipe(
            ShapedRecipe(
                result=self.bucket.get("fisherman_hat"),
                pattern=[
                    " W ",
                    "WFW",
                ],
                key={
                    "W": "minecraft:leather",
                    "F": "minecraft:cod",
                },
            )
        )