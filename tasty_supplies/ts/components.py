from typing import Any, Dict, Iterable

from .declaration import Declaration
from .translatable import Translatable
from .utils import title_case

DEFAULT_MAX_STACK_SIZE = 64
RARITIES = ("common", "uncommon", "rare", "epic")
DISABLED_COMPONENTS = ()


def build(item_id: str, item_type: str, declaration: Declaration) -> Dict[str, Any]:
    """The components of an item, without removals and without ``ts_hash``."""
    
    from . import Translatable

    components: Dict[str, Any] = dict(declaration.components)

    _add_effects(item_id, item_type, components, declaration)

    if "food" in components:
        components.setdefault("consumable", {})
    if "max_damage" in components or "equippable" in components:
        components.setdefault("max_stack_size", 1)

    components.setdefault("max_stack_size", DEFAULT_MAX_STACK_SIZE)
    components.setdefault("item_name", Translatable(f"ts.item.{item_id}.name", default=title_case(item_id)))
    components.setdefault("rarity", "common")

    custom_data = dict(components.get("custom_data", {}))
    custom_data["ts_name"] = item_id
    components["custom_data"] = custom_data
    components["custom_model_data"] = {"strings": [f"tasty_supplies/{item_id}"]}

    return components


def _add_effects(item_id: str, item_type: str, components: Dict[str, Any], declaration: Declaration) -> None:
    entries = list(declaration.consume_effects)

    if declaration.apply_effects:
        grouped: Dict[Any, list] = {}
        for probability, effect in declaration.apply_effects:
            grouped.setdefault(probability, []).append(effect)

        for probability, effects in grouped.items():
            entry: Dict[str, Any] = {"type": "apply_effects", "effects": effects}
            if probability is not None:
                entry["probability"] = probability
            entries.append(entry)

    if entries:
        consumable = dict(components.get("consumable", {}))
        consumable["on_consume_effects"] = (
            consumable.get("on_consume_effects", []) + entries
        )
        components["consumable"] = consumable

    if declaration.potion_effects:
        contents = dict(components.get("potion_contents", {}))
        contents["custom_effects"] = (
            contents.get("custom_effects", []) + declaration.potion_effects
        )
        components["potion_contents"] = contents
        components["potion_contents"]["potion"] = "water"
        components["potion_contents"]["custom_color"] = 16777215
        components["potion_contents"]["custom_name"] = item_id

        Translatable(f"item.minecraft.{item_type}.effect.{item_id}", default=title_case(item_id))


def with_removals(
    components: Dict[str, Any], extra: Iterable[str] = ()
) -> Dict[str, Any]:
    """Add component removals, which a patch accepts but a predicate does not."""

    patch = dict(components)
    for name in (*DISABLED_COMPONENTS, *extra):
        patch[f"!minecraft:{name.removeprefix('minecraft:')}"] = {}
    return patch
