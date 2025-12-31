import hashlib
import json
from typing import Any, Dict, Optional

from beet import Function, Model, ItemModel

from ..constants import MINECRAFT_NAMESPACE
from .context import TSContext
from ..utils import to_absolute_path, to_item_repr
from ..logger import log
from ..constants import (
    DEFAULT_MAX_STACK_SIZE,
    DEFAULT_BASE_ITEM,
    TASTY_SUPPLIES_NAMESPACE,
    COMPONENT_MAX_STACK_SIZE,
    COMPONENT_CUSTOM_NAME,
    COMPONENT_CUSTOM_MODEL_DATA,
    TEXT_COLOR_WHITE,
    TEXT_ITALIC_FALSE,
    MODEL_TYPE_ITEM,
    MODEL_TYPE_SELECT,
    MODEL_TYPE_MODEL,
    MODEL_TYPE_GENERATED,
)


class Item:
    """Represents a custom Minecraft item with its visual properties.

    Items are independent from recipes and can be referenced by any recipe.
    They define how the item looks and which base Minecraft item it uses.
    """

    def __init__(
        self,
        item_name: str,
        base_item: str = DEFAULT_BASE_ITEM,
        texture_path: Optional[str] = None,
        model_type: str = MODEL_TYPE_ITEM,
        max_stack_size: int = DEFAULT_MAX_STACK_SIZE,
        **components: Any,
    ):
        """Initialize a custom item.

        Args:
            item_name: The unique identifier for this custom item
            base_item: The vanilla Minecraft item to use as a base
            texture_path: Optional custom texture path
            model_type: Either "item" or "block" to determine texture location
            **components: Item components (food, consumable, max_stack_size, etc.)
        """
        self.name = item_name
        self.base_item = base_item
        self.texture_path = (
            texture_path or f"{TASTY_SUPPLIES_NAMESPACE}:{model_type}/{item_name}"
        )
        self.model_type = model_type

        self.components: Dict[str, Any] = {}
        self.components = self.components | components

        from ..constants import COMPONENT_FOOD, COMPONENT_CONSUMABLE

        if (
            COMPONENT_FOOD in self.components
            and COMPONENT_CONSUMABLE not in self.components
        ):
            self.components[COMPONENT_CONSUMABLE] = {}

        self.components[COMPONENT_MAX_STACK_SIZE] = max_stack_size

        if not self.components.get("custom_data"):
            self.components["custom_data"] = {}

        self.components["custom_data"]["ts_name"] = self.name

        if (
            "banner_pattern" in self.base_item
            and not "provides_banner_patterns" in self.components
        ):
            self.components["provides_banner_patterns"] = "#minecraft:pattern_item/none"

        self.components.setdefault(
            "tooltip_display",
            {
                "hidden_components": [
                    "minecraft:provides_banner_patterns",
                ]
            },
        )

        display_name = " ".join(word.capitalize() for word in item_name.split("_"))
        self.components[COMPONENT_CUSTOM_NAME] = {
            "text": display_name,
            "italic": TEXT_ITALIC_FALSE,
            "color": TEXT_COLOR_WHITE,
        }

    def register(self, ctx: TSContext):
        """Register this item with the Beet context.

        This creates the necessary model and item_model files and registers
        the custom model data case with the base item.

        Args:
            ctx: The Tasty Supplies context
        """
        if not ctx.assets["tasty_supplies"].models.get(f"item/{self.name}"):
            ctx.assets["tasty_supplies"].models[f"item/{self.name}"] = self._get_model()

        ctx.assets["tasty_supplies"].item_models[self.name] = self._get_item_model(ctx)
        self._register_model_case(ctx)
        if not self._texture_path_exist(ctx):
            log.warning(f"Non-existent texture for item '{self.name}.'")

        self._setup_sha1_updater(ctx)

    def _texture_path_exist(self, ctx: TSContext) -> bool:
        return not ctx.assets.textures.get(self.texture_path) is None

    def _register_model_case(self, ctx: TSContext):
        item_models: dict = ctx.assets["minecraft"].item_models
        if item_models.get(self.base_item) is None:
            self.create_base_item_model(ctx)

        item_model: dict = ctx.assets["minecraft"].item_models[self.base_item].data

        if item_model["model"].get("cases") is None:
            raise ValueError(f"Item model cases not found for {self.base_item}.")

        model_path = f"{TASTY_SUPPLIES_NAMESPACE}:{MODEL_TYPE_ITEM}/{self.name}"
        for candidate in item_model["model"]["cases"]:
            if candidate["model"]["model"] == model_path:
                log.warning(
                    f"Item model case for {self.name} already exists in "
                    f"minecraft:items/{self.base_item}. Skipping model registration."
                )
                return

        item_model["model"]["cases"].append(
            {
                "when": f"{TASTY_SUPPLIES_NAMESPACE}/{self.name}",
                "model": {
                    "type": MODEL_TYPE_MODEL,
                    "model": model_path,
                },
            }
        )

    def create_base_item_model(self, ctx: TSContext) -> None:
        """Create the base item model with custom_model_data selection.

        Args:
            ctx: The Tasty Supplies context

        Raises:
            ValueError: If base item model not found in vanilla assets
        """
        from core.constants import MINECRAFT_NAMESPACE

        base_item_model = ctx.vanilla.assets.item_models.get(
            to_absolute_path(self.base_item)
        )
        if base_item_model is None:
            raise ValueError(
                f"Base item model for {self.base_item} not found in vanilla assets."
            )

        ctx.assets[MINECRAFT_NAMESPACE].item_models[self.base_item] = ItemModel(
            {
                "model": {
                    "type": MODEL_TYPE_SELECT,
                    "property": f"{MINECRAFT_NAMESPACE}:{COMPONENT_CUSTOM_MODEL_DATA}",
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
            "parent": MODEL_TYPE_GENERATED,
            "textures": {"layer0": self.texture_path},
        }
        return Model(json_model, f"{self.name}.json")

    def _get_item_model(self, _ctx: TSContext) -> ItemModel:
        """Generate the item_model JSON.

        Returns:
            ItemModel: The Beet ItemModel object for this item
        """
        return ItemModel(
            {
                "model": {
                    "type": MODEL_TYPE_MODEL,
                    "model": f"{TASTY_SUPPLIES_NAMESPACE}:{MODEL_TYPE_ITEM}/{self.name}",
                }
            }
        )

    def _setup_sha1_updater(self, ctx: TSContext) -> None:
        """Setup SHA1 updater functions.

        Args:
            ctx: The Tasty Supplies context
        """
        sha1_check_func = ctx.data["tasty_supplies"].functions.get("updater/check_sha1")
        sha1_check_func.append(
            Function(
                'execute if data storage tasty_supplies:updater temp{hash: "'
                + self._to_sha1()
                + '"} run return 1'
            )
        )

        item_replace_func = ctx.data["tasty_supplies"].functions.get(
            "updater/replace_item"
        )
        item_replace_func.append(
            Function(
                (
                    '$execute if data storage tasty_supplies:updater temp{item_name: "'
                    + self.name
                    + '"} run item replace $(target) $(path) with '
                    + to_item_repr(self)
                    + " $(count)"
                ),
                (
                    '$execute if data storage tasty_supplies:updater temp{item_name: "'
                    + self.name
                    + '"} run return 0'
                ),
            ),
        )

    def to_ingredient(self) -> Dict[str, Any]:
        """Convert this item to a recipe ingredient format.

        Returns:
            dict: The ingredient data for use in recipes
        """
        from core.constants import MINECRAFT_NAMESPACE

        return {
            "id": f"{MINECRAFT_NAMESPACE}:{self.base_item}",
            "components": {
                f"{MINECRAFT_NAMESPACE}:{COMPONENT_CUSTOM_MODEL_DATA}": {
                    "strings": [f"{TASTY_SUPPLIES_NAMESPACE}/{self.name}"]
                }
            },
        }

    def to_result(self, count: int = 1) -> Dict[str, Any]:
        result = self.nbt
        result["count"] = count
        return result

    def _raw_nbt(self, count: int = 1) -> dict:
        nbt = {
            "id": f"{MINECRAFT_NAMESPACE}:{self.base_item}",
            "count": count,
            "components": self.custom_model_data | self.components,
        }
        nbt = json.loads(json.dumps(nbt, sort_keys=True))
        return nbt

    @property
    def nbt(self) -> dict:
        nbt = self._raw_nbt()
        nbt["components"].setdefault("custom_data", {})["ts_hash"] = self._to_sha1()
        return nbt

    @property
    def custom_model_data(self) -> dict:
        return {
            f"{COMPONENT_CUSTOM_MODEL_DATA}": {
                "strings": [f"{TASTY_SUPPLIES_NAMESPACE}/{self.name}"]
            }
        }

    @property
    def icon(self) -> dict:
        return self.nbt

    @property
    def predicate(self) -> dict:
        return {
            "items": self.base_item,
            "components": self.custom_model_data | self.components,
        }

    def entry(
        self,
        weight: int = 1,
        min_count: float = 1.0,
        max_count: float = 1.0,
        min_looting: float = 0.0,
        max_looting: float = 0.0,
        **kwargs,
    ) -> dict:
        entry = {
            "type": "minecraft:item",
            "name": f"{MINECRAFT_NAMESPACE}:{self.base_item}",
            "functions": [
                {
                    "function": "minecraft:set_components",
                    "components": self.custom_model_data | self.components,
                }
            ],
            "weight": int(weight),
        }

        if min_count == max_count:
            entry["functions"].append(
                {
                    "function": "minecraft:set_count",
                    "add": False,
                    "count": min_count,
                }
            )
        else:
            entry["functions"].append(
                {
                    "function": "minecraft:set_count",
                    "add": False,
                    "count": {
                        "type": "minecraft:uniform",
                        "min": min_count,
                        "max": max_count,
                    },
                }
            )

        if min_looting > 0 or max_looting > 0:
            entry["functions"].append(
                {
                    "function": "minecraft:enchanted_count_increase",
                    "enchantment": "minecraft:looting",
                    "count": {
                        "type": "minecraft:uniform",
                        "min": min_looting,
                        "max": max_looting,
                    },
                }
            )

        for key, value in kwargs.items():
            entry["functions"].append(
                {
                    "function": key,
                    **value,
                }
            )

        return entry

    def _to_sha1(self) -> str:
        raw_nbt = self._raw_nbt()
        canonical = json.dumps(
            raw_nbt,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        sha1_hash = hashlib.sha1()
        sha1_hash.update(canonical)
        return sha1_hash.hexdigest()


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
        **components: Any,
    ):
        """Initialize a block item.

        Args:
            item_name: The unique identifier for this custom item
            base_item: The vanilla Minecraft item to use as a base (default: "armor_stand")
            **components: Item components including custom_data, entity_data, etc.
        """
        from core.constants import MODEL_TYPE_BLOCK

        super().__init__(
            item_name=item_name,
            base_item=base_item,
            texture_path=f"{TASTY_SUPPLIES_NAMESPACE}:{MODEL_TYPE_BLOCK}/{item_name}",
            model_type=MODEL_TYPE_BLOCK,
            **components,
        )
