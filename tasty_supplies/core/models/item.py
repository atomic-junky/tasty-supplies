from beet import Model, ItemModel

from .context import TSContext
from .recipe import _Recipe, FakeRecipe
from .tools import to_absolute_path
from core.logger import log


class Item:
    def __init__(
        self, item_name: str, recipe: _Recipe = FakeRecipe(), base_item: str = "bread"
    ):
        self.name = item_name
        self.recipe = recipe
        self.base_item = base_item

    def register(self, ctx: TSContext):
        if not self.name in ctx.showcase_items:
            ctx.showcase_items.append(self.name)

        ctx.assets["tasty_supplies"].models[f"item/{self.name}"] = self._get_model()
        ctx.assets["tasty_supplies"].item_models[self.name] = self._get_item_model()
        self._register_model_case(ctx)

        if not isinstance(self.recipe, FakeRecipe):
            self.recipe._register(self.name, self.base_item, ctx)

    def _register_model_case(self, ctx: TSContext):
        item_models: dict = ctx.assets["minecraft"].item_models
        if item_models.get(self.base_item) is None:
            self.create_base_item_model(ctx)

        item_model: dict = ctx.assets["minecraft"].item_models[self.base_item].data

        if item_model["model"].get("cases", None) is None:
            raise ValueError(f"Item model cases not found for {self.base_item}.")

        for candidate in item_model["model"]["cases"]:
            if candidate["model"]["model"] == f"tasty_supplies:item/{self.name}":
                log.warning(
                    f"Item model case for {self.name} already exists in minecraft:items/{self.base_item}. Skipping model registration."
                )
                return

        item_model["model"]["cases"].append(
            {
                "when": f"tasty_supplies/{self.name}",
                "model": {
                    "type": "minecraft:model",
                    "model": f"tasty_supplies:item/{self.name}",
                },
            }
        )

    def create_base_item_model(self, ctx: TSContext) -> None:
        base_item_model = ctx.vanilla.assets.item_models.get(
            to_absolute_path(self.base_item)
        )
        if base_item_model is None:
            raise ValueError(
                f"Base item model for {self.base_item} not found in vanilla assets."
            )

        ctx.assets["minecraft"].item_models[self.base_item] = ItemModel(
            {
                "model": {
                    "type": "minecraft:select",
                    "property": "minecraft:custom_model_data",
                    "cases": [],
                    "fallback": base_item_model.data["model"],
                },
            }
        )

    def _get_model(self) -> Model:
        json_model = {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"tasty_supplies:item/{self.name}"},
        }
        return Model(json_model, f"{self.name}.json")

    def _get_item_model(self) -> ItemModel:
        return ItemModel(
            {
                "model": {
                    "type": "minecraft:model",
                    "model": "tasty_supplies:item/" + self.name,
                }
            }
        )


class BlockItem(Item):
    def __init__(
        self,
        item_name: str,
        recipe: _Recipe = FakeRecipe(),
        base_item: str = "armor_stand",
    ):
        super().__init__(item_name, recipe, base_item)

    def _get_model(self) -> Model:
        json_model = {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"tasty_supplies:block/{self.name}"},
        }
        return Model(json_model, f"{self.name}.json")

    def _get_item_model(self) -> ItemModel:
        return ItemModel(
            {
                "model": {
                    "type": "minecraft:model",
                    "model": "tasty_supplies:item/" + self.name,
                }
            }
        )
