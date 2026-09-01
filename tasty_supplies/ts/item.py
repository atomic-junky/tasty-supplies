"""How a declared class turns into pack data.

``Item`` only exposes derived views; the ``emit`` plugin writes them out.
"""

import hashlib
import json
from typing import Any, Dict, List, Optional, Union

from . import bases
from . import components as components_module
from .bases import Base
from .declaration import Declarable
from .utils import components_to_snbt


class Item(Declarable, abstract=True):
    """A custom item: a vanilla item plus components."""

    base: Union[Base, str] = bases.BREAD
    parent_model: str = "minecraft:item/generated"
    #: Defaults to ``tasty_supplies:item/<id>``.
    texture: Optional[str] = None
    #: Whether the recipes producing this item appear in the recipe book.
    book: bool = True

    def __init__(self) -> None:
        self.declaration = type(self).declaration()
        self.components: Dict[str, Any] = components_module.build(
            self.id, self.declaration
        )

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.id}>"

    @property
    def support(self) -> Base:
        return Base.of(self.base)

    @property
    def texture_path(self) -> str:
        return self.texture or f"tasty_supplies:item/{self.id}"

    @property
    def model_path(self) -> str:
        return f"tasty_supplies:item/{self.id}"

    def recipes(self) -> List[Any]:
        """Recipes declared by decorator; a family may override this."""

        return list(self.declaration.recipes)

    @property
    def patch(self) -> Dict[str, Any]:
        """Components as applied to an item: removals included, no hash."""

        return components_module.with_removals(
            self.components, self.declaration.disabled
        )

    @property
    def sha1(self) -> str:
        """Fingerprint of the item, computed on everything but the hash itself."""

        canonical = json.dumps(
            self._raw_stack(), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha1(canonical).hexdigest()

    def _raw_stack(self, count: int = 1) -> Dict[str, Any]:
        stack = {
            "id": f"minecraft:{self.support.id}",
            "count": count,
            "components": self.patch,
        }
        return json.loads(json.dumps(stack, sort_keys=True))

    def stack(self, count: int = 1) -> Dict[str, Any]:
        """The item as an ``ItemStack`` JSON, fingerprint included."""

        stack = self._raw_stack(count)
        stack["components"].setdefault("custom_data", {})["ts_hash"] = self.sha1
        return stack

    @property
    def icon(self) -> Dict[str, Any]:
        return self.stack()

    @property
    def predicate(self) -> Dict[str, Any]:
        """Item test for advancements, matching exactly, so without removals."""

        return {"items": self.support.id, "components": self.components}

    @property
    def give(self) -> str:
        """``<support>[<components>]``, for ``give`` and ``item replace``."""

        stack = self.stack()
        return f"{stack['id']}[{components_to_snbt(stack['components'])}]"

    def entry(
        self,
        weight: int = 1,
        min_count: float = 1.0,
        max_count: float = 1.0,
        min_looting: float = 0.0,
        max_looting: float = 0.0,
        **functions: dict,
    ) -> Dict[str, Any]:
        """A loot table entry yielding this item."""

        entry: Dict[str, Any] = {
            "type": "minecraft:item",
            "name": f"minecraft:{self.support.id}",
            "functions": [
                {"function": "minecraft:set_components", "components": self.patch}
            ],
            "weight": int(weight),
        }

        if min_count == max_count:
            count: Any = min_count
        else:
            count = {"type": "minecraft:uniform", "min": min_count, "max": max_count}
        entry["functions"].append(
            {"function": "minecraft:set_count", "add": False, "count": count}
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

        for name, options in functions.items():
            entry["functions"].append({"function": name, **options})

        return entry

    @property
    def model(self) -> Dict[str, Any]:
        """``assets/tasty_supplies/models/item/<id>.json``."""

        return {
            "parent": self.parent_model,
            "textures": {"layer0": self.texture_path},
        }

    @property
    def item_model(self) -> Dict[str, Any]:
        """``assets/tasty_supplies/items/<id>.json``."""

        return {"model": {"type": "minecraft:model", "model": self.model_path}}

    @property
    def model_case(self) -> Dict[str, Any]:
        """The case added to the support definition, keyed by model data."""

        return {
            "when": f"tasty_supplies/{self.id}",
            "model": {"type": "minecraft:model", "model": self.model_path},
        }
