import json
from logging import log
from typing import Any

from beet import ItemModel

from core import (
    TSContext,
    TASTY_SUPPLIES_NAMESPACE,
    Item,
    ShapedRecipe,
    Category,
    Bucket,
)
from core.constants import MODEL_TYPE_ITEM, MODEL_TYPE_MODEL


class EquipementItem(Item):
    def __init__(
        self, item_name: str, slot: str, equipement_id: str, **components: Any
    ):
        self.slot = slot

        super().__init__(
            item_name=item_name,
            base_item=self._get_base_item(),
            max_stack_size=1,
            equippable={"slot": slot, "dispensable": True, "swappable": True},
            # item_model=f"equipement/{item_name}",
            **components,
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

    def _register_model_case(self, ctx: TSContext) -> ItemModel:
        """Generate the item_model JSON.

        Returns:
            ItemModel: The Beet ItemModel object for this item
        """

        item_models: dict = ctx.assets["minecraft"].item_models
        if item_models.get(self.base_item) is None:
            self.create_base_item_model(ctx)

        item_model: dict = ctx.assets["minecraft"].item_models[self.base_item].data

        if item_model["model"].get("cases") is None:
            raise ValueError(f"Item model cases not found for {self.base_item}.")

        model_path = f"{TASTY_SUPPLIES_NAMESPACE}:{MODEL_TYPE_ITEM}/{self.name}"
        for candidate in item_model["model"]["cases"]:
            if (
                "model" in candidate["model"]
                and candidate["model"]["model"] == model_path
            ):
                log.warning(
                    f"Item model case for {self.name} already exists in "
                    f"minecraft:items/{self.base_item}. Skipping model registration."
                )
                return

        item_model["model"]["cases"].append(
            {
                "when": f"{TASTY_SUPPLIES_NAMESPACE}/{self.name}",
                "model": {
                    "type": "minecraft:select",
                    "property": "minecraft:display_context",
                    "cases": [
                        {
                            "when": self.slot,
                            "model": {
                                "type": MODEL_TYPE_MODEL,
                                "model": f"{TASTY_SUPPLIES_NAMESPACE}:{MODEL_TYPE_ITEM}/equipement/{self.name}",
                            },
                        }
                    ],
                    "fallback": {
                        "type": MODEL_TYPE_MODEL,
                        "model": f"{TASTY_SUPPLIES_NAMESPACE}:{MODEL_TYPE_ITEM}/{self.name}",
                    },
                },
            }
        )


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
        self.add_item(EquipementItem("farmer_hat", slot="head", equipement_id="farmer"))
        # self.add_item(Item("farmer_hat", base_item="leather_helmet", max_stack_size=1))

        self.add_item(
            EquipementItem("fisherman_hat", slot="head", equipement_id="fisherman")
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
