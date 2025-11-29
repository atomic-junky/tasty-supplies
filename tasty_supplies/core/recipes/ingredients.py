"""Ingredients category - contains base ingredient items and their recipes.

This module defines raw and processed ingredients used in other recipes.
All items and recipes are managed through the Bucket system.
"""

from .. import (
    Bucket,
    Item,
    AutoCookingRecipe,
    CuttingBoardRecipe,
    ShapedRecipe,
    Category,
    aliases,
)


class Ingredients(Category):
    """Category for ingredient items."""

    def __init__(self, bucket: Bucket):
        """Initialize Ingredients category with bucket reference.

        Args:
            bucket: The Bucket instance to store items and recipes
        """
        super().__init__("Ingredients", bucket)

    def create_items(self):
        """Create all ingredient items and add them to the bucket."""
        self.add_item(
            Item(
                "raw_bacon",
                food={"nutrition": 1.5, "saturation": 0.3},
                base_item=aliases.RAW_BACON,
            )
        )

        self.add_item(
            Item(
                "cooked_bacon",
                food={"nutrition": 4, "saturation": 6.4},
                base_item=aliases.COOKED_BACON,
            )
        )

        self.add_item(
            Item(
                "butter",
                base_item=aliases.BUTTER,
                food={"nutrition": 2, "saturation": 1.2},
                consumable={"on_consume_effects": [{"type": "clear_all_effects"}]},
            )
        )
        self.add_item(Item("pie_crust", base_item=aliases.PIE_CRUST))
        self.add_item(Item("rice", base_item=aliases.RICE))
        self.add_item(
            Item(
                "cooked_rice",
                base_item=aliases.COOKED_RICE,
                food={"nutrition": 2, "saturation": 3.2},
            )
        )
        self.add_item(
            Item(
                "raw_cod_slice",
                base_item=aliases.RAW_COD_SLICE,
                food={"nutrition": 1, "saturation": 0.8},
            )
        )
        self.add_item(
            Item(
                "raw_salmon_slice",
                base_item=aliases.RAW_SALMON_SLICE,
                food={"nutrition": 1, "saturation": 0.8},
            )
        )
        self.add_item(
            Item(
                "ice_cream_cone",
                food={"nutrition": 2, "saturation": 0.4},
            )
        )
        self.add_item(
            Item(
                "tentacle",
                base_item=aliases.TENTACLE,
                food={"nutrition": 3, "saturation": 2.4},
                consumable={},
            )
        )
        self.add_item(
            Item(
                "guardian_tail",
                base_item=aliases.GUARDIAN_TAIL,
                food={"nutrition": 2, "saturation": 1.6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:mining_fatigue",
                                    "duration": 600,
                                }
                            ],
                        }
                    ]
                },
            )
        )
        self.add_item(
            Item(
                "barnacle_thong",
                base_item=aliases.BARNACLE_TENTACLE,
                food={"nutrition": 1, "saturation": 0.8},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:nausea",
                                    "duration": 150,
                                }
                            ],
                        }
                    ]
                },
            )
        )
        self.add_item(
            Item(
                "glare_eye",
                base_item=aliases.GLARE_EYE,
                food={"nutrition": 1, "saturation": 0.6},
                consumable={
                    "on_consume_effects": [
                        {
                            "type": "apply_effects",
                            "effects": [
                                {
                                    "id": "minecraft:night_vision",
                                    "duration": 100,
                                }
                            ],
                        }
                    ]
                },
            )
        )
        self.add_item(Item("great_hunger_teeth", base_item=aliases.GREAT_HUNGER_TEETH))

    def create_recipes(self):
        """Create all ingredient recipes and add them to the bucket."""

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient="porkchop",
                result=self.bucket.get("raw_bacon"),
                result_count=2,
            )
        )

        self.add_recipe(
            AutoCookingRecipe(
                ingredient=self.bucket.get_ingredient("raw_bacon"),
                result=self.bucket.get("cooked_bacon"),
                base_cooking_time=75,
                experience=0.2,
            )
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient="wheat",
                result=self.bucket.get("rice"),
                result_count=4,
            ),
        )

        self.add_recipe(
            AutoCookingRecipe(
                ingredient=self.bucket.get_ingredient("rice"),
                result=self.bucket.get("cooked_rice"),
                base_cooking_time=150,
                experience=0.25,
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient="cod",
                result=self.bucket.get("raw_cod_slice"),
                result_count=2,
            ),
        )

        self.add_recipe(
            CuttingBoardRecipe(
                ingredient="salmon",
                result=self.bucket.get("raw_salmon_slice"),
                result_count=2,
            ),
        )

        self.add_recipe(
            ShapedRecipe(
                key={"W": "wheat"},
                pattern=["W", "W", "W"],
                result=self.bucket.get("ice_cream_cone"),
                result_count=3,
            ),
        )
