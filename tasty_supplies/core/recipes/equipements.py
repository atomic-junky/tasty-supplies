from logging import log
from beet import ItemModel

from core import (
    TSContext,
    Item,
    ShapedRecipe,
    Category,
    Bucket,
)


class EquipementItem(Item):
    def __init__(
        self,
        item_name: str,
        slot: str,
        equipement_id: str,
        *component: dict,
        **components: dict,
    ):
        self.slot = slot
        for data in component:
            for key, value in data.items():
                components[key] = value

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
            case "chest":  # Useless
                return "leather_chestplate"
            case "legs":  # Useless
                return "leather_leggings"
            case "feet":  # Useless
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

        model_path = f"tasty_supplies:item/{self.name}"
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
                "when": f"tasty_supplies/{self.name}",
                "model": {
                    "type": "minecraft:select",
                    "property": "minecraft:display_context",
                    "cases": [
                        {
                            "when": self.slot,
                            "model": {
                                "type": "minecraft:model",
                                "model": f"tasty_supplies:item/equipement/{self.name}",
                            },
                        }
                    ],
                    "fallback": {
                        "type": "minecraft:model",
                        "model": f"tasty_supplies:item/{self.name}",
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

        ## Equipment other than helmets cannot be added without mods due to technical limitations.

        # self.add_item(
        #     EquipementItem("fisherman_apron", slot="chest", equipement_id="fisherman")
        # )

        self.add_item(
            EquipementItem(
                "farmer_hat",
                "head",
                "farmer",
            )
        )

        # self.add_item(
        #     EquipementItem("butcher_apron", slot="chest", equipement_id="butcher")
        # )

        self.add_item(
            EquipementItem(
                "fisherman_hat",
                "head",
                "fisherman",
            )
        )

    def create_recipes(self):
        """Create all equipement recipes."""
        self.add_recipe(
            ShapedRecipe(
                result=self.bucket.get("farmer_hat"),
                pattern=[
                    " W ",
                    "WWW",
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
