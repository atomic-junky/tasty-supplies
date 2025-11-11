"""Crops category - defines seed and crop items in a data-driven fashion."""

from __future__ import annotations

from typing import Dict, List

from .. import Bucket, Category, Item, ShapelessRecipe
from ..aliases import CORN, CABBAGE, TOMATO
from ..models.context import TSContext
from ..models.crop import CropDefinition, CropManager, DropConfig


class Crops(Category):
    """Category responsible for registering crop items and recipes."""

    def __init__(self, bucket: Bucket):
        super().__init__("Crops", bucket)
        self.definitions: List[CropDefinition] = self._build_definitions()

    def _build_definitions(self) -> List[CropDefinition]:
        return [
            CropDefinition(
                name="tomato",
                seed_base_item="wheat_seeds",
                seed_texture="minecraft:item/beetroot_seeds",
                produce_base_item=TOMATO,
                produce_texture="minecraft:item/beetroot",
                stage_textures=[
                    "minecraft:block/beetroots_stage0",
                    "minecraft:block/beetroots_stage1",
                    "minecraft:block/beetroots_stage2",
                    "minecraft:block/beetroots_stage3",
                ],
                growth_interval=120,
                produce_components={
                    "food": {"nutrition": 3, "saturation": 2.4},
                },
                harvest_drops=[
                    DropConfig(item="tomato", min_count=1, max_count=3),
                    DropConfig(
                        item="tomato_seeds", min_count=0, max_count=1, chance=0.5
                    ),
                ],
            ),
            CropDefinition(
                name="corn",
                seed_base_item="wheat_seeds",
                seed_texture="minecraft:item/melon_seeds",
                produce_base_item=CORN,
                produce_texture="minecraft:item/golden_carrot",
                stage_textures=[
                    "minecraft:block/wheat_stage0",
                    "minecraft:block/wheat_stage2",
                    "minecraft:block/wheat_stage4",
                    "minecraft:block/wheat_stage7",
                ],
                growth_interval=160,
                produce_components={
                    "food": {"nutrition": 5, "saturation": 6.0},
                },
                harvest_drops=[
                    DropConfig(item="corn", min_count=2, max_count=4),
                    DropConfig(
                        item="corn_seeds", min_count=1, max_count=2, chance=0.75
                    ),
                ],
            ),
            CropDefinition(
                name="cabbage",
                seed_base_item="wheat_seeds",
                seed_texture="tasty_supplies:item/cabbage_seeds",
                produce_base_item=CABBAGE,
                produce_texture="minecraft:item/kelp",
                stage_textures=[
                    "tasty_supplies:block/cabbages_stage0",
                    "tasty_supplies:block/cabbages_stage1",
                    "tasty_supplies:block/cabbages_stage2",
                    "tasty_supplies:block/cabbages_stage3",
                    "tasty_supplies:block/cabbages_stage4",
                    "tasty_supplies:block/cabbages_stage5",
                    "tasty_supplies:block/cabbages_stage6",
                    "tasty_supplies:block/cabbages_stage7",
                ],
                growth_interval=100,
                produce_components={
                    "food": {"nutrition": 2, "saturation": 1.2},
                },
                harvest_drops=[
                    DropConfig(item="cabbage", min_count=1, max_count=2),
                    DropConfig(
                        item="cabbage_seeds", min_count=1, max_count=1, chance=0.6
                    ),
                ],
            ),
        ]

    def create_items(self) -> None:
        for definition in self.definitions:
            seed_components: Dict[str, object] = {
                "custom_data": {"tasty_supplies": {"seed": definition.name}},
            }
            self.add_item(
                Item(
                    definition.seed_item_name,
                    base_item=definition.seed_base_item,
                    texture_path=definition.seed_texture,
                    **seed_components,
                )
            )

            if definition.create_produce_item:
                produce_components = definition.produce_components or {}
                self.add_item(
                    Item(
                        definition.produce_item_name,
                        base_item=definition.produce_base_item,
                        texture_path=definition.produce_texture,
                        **produce_components,
                    )
                )

    def create_recipes(self) -> None:
        for definition in self.definitions:
            seed_item = self.bucket.get(definition.seed_item_name)
            produce_base = self.bucket.get_ingredient(definition.produce_item_name)
            if produce_base and seed_item:
                self.add_recipe(
                    ShapelessRecipe(
                        ingredients=[produce_base],
                        result=seed_item,
                        result_count=2,
                        recipe_id=f"{definition.seed_item_name}_from_{definition.produce_item_name}",
                    )
                )

    def build_manager(self, ctx: TSContext) -> CropManager:
        """Create the :class:`CropManager` for this category."""

        return CropManager(ctx, self.bucket, self.definitions)
