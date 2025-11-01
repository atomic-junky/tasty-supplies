from beet import Model, ItemModel

from .context import TSContext
from core.utils import to_absolute_path
from core.logger import log


class Item:
    """Represents a custom Minecraft item with its visual properties.

    Items are independent from recipes and can be referenced by any recipe.
    They define how the item looks and which base Minecraft item it uses.
    """

    def __init__(
        self,
        item_name: str,
        base_item: str = "bread",
        texture_path: str = None,
        model_type: str = "item",
        **components,
    ):
        """Initialize a custom item.

        Args:
            item_name: The unique identifier for this custom item
            base_item: The vanilla Minecraft item to use as a base (default: "bread")
            texture_path: Optional custom texture path (default: "tasty_supplies:item/{item_name}")
            model_type: Either "item" or "block" to determine texture location
            **components: Item components (food, consumable, max_stack_size, etc.)
        """
        self.name = item_name
        self.base_item = base_item
        self.texture_path = texture_path or f"tasty_supplies:{model_type}/{item_name}"
        self.model_type = model_type

        # Set default max_stack_size if not provided
        if "max_stack_size" not in components:
            components["max_stack_size"] = 64

        # Auto-generate display name if not provided
        if "custom_name" not in components:
            # Convert snake_case to Title Case
            display_name = " ".join(word.capitalize() for word in item_name.split("_"))
            components["custom_name"] = {
                "text": display_name,
                "italic": False,
                "color": "white",
            }

        self.components = components

    def register(self, ctx: TSContext):
        """Register this item with the Beet context.

        This creates the necessary model and item_model files and registers
        the custom model data case with the base item.

        Args:
            ctx: The Tasty Supplies context
        """
        ctx.assets["tasty_supplies"].models[f"item/{self.name}"] = self._get_model()
        ctx.assets["tasty_supplies"].item_models[self.name] = self._get_item_model()
        self._register_model_case(ctx)

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
        """Generate the item model JSON.

        Returns:
            Model: The Beet Model object for this item
        """
        json_model = {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": self.texture_path},
        }
        return Model(json_model, f"{self.name}.json")

    def _get_item_model(self) -> ItemModel:
        """Generate the item_model JSON.

        Returns:
            ItemModel: The Beet ItemModel object for this item
        """
        return ItemModel(
            {
                "model": {
                    "type": "minecraft:model",
                    "model": "tasty_supplies:item/" + self.name,
                }
            }
        )

    def to_ingredient(self) -> dict:
        """Convert this item to a recipe ingredient format.

        Returns:
            dict: The ingredient data for use in recipes
        """
        return {
            "id": f"minecraft:{self.base_item}",
            "components": {
                "minecraft:custom_model_data": {
                    "strings": [f"tasty_supplies/{self.name}"]
                }
            },
        }

    def to_result(self, count: int = 1) -> dict:
        """Convert this item to a recipe result format.

        Uses the item's stored components to ensure consistency across all uses.

        Args:
            count: Number of items to produce (default: 1)

        Returns:
            dict: The result data for use in recipes and commands
        """
        result = {
            "id": f"minecraft:{self.base_item}",
            "count": count,
            "components": {
                "minecraft:custom_model_data": {
                    "strings": [f"tasty_supplies/{self.name}"]
                },
                **self.components,
            },
        }
        return result


class BlockItem(Item):
    """Represents a custom item that uses block textures.

    This is a convenience class for items that should reference
    textures from the block texture folder instead of the item folder.
    BlockItems can also have special components for entity placement.
    """

    def __init__(
        self,
        item_name: str,
        base_item: str = "armor_stand",
        **components,
    ):
        """Initialize a block item.

        Args:
            item_name: The unique identifier for this custom item
            base_item: The vanilla Minecraft item to use as a base (default: "armor_stand")
            **components: Item components including custom_data, entity_data, etc.
        """
        super().__init__(
            item_name=item_name,
            base_item=base_item,
            texture_path=f"tasty_supplies:block/{item_name}",
            model_type="block",
            **components,
        )
