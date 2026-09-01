"""Building the components of an item, in four layers.

1. core: ``custom_model_data`` and ``custom_data.ts_name``, always present;
2. defaults: ``item_name``, ``rarity``, ``max_stack_size``, set when missing;
3. traits: conditional, such as ``food`` implying ``consumable``;
4. removals: ``DISABLED_COMPONENTS``, emitted as ``"!minecraft:x"``.

Precedence: core > explicit declaration > trait > default.
"""

from typing import Any, Dict, Iterable

from .declaration import Declaration
from .utils import title_case

DEFAULT_MAX_STACK_SIZE = 64

RARITIES = ("common", "uncommon", "rare", "epic")

#: Vanilla components dropped from every item, so that an item based on a
#: banner pattern does not stay usable on a loom. Empty until the change lands
#: with its own in-game test: it rewrites the hash of every item.
#: Candidates: ``provides_banner_patterns``, ``provides_trim_material``.
DISABLED_COMPONENTS = ()


def build(item_id: str, declaration: Declaration) -> Dict[str, Any]:
    """The components of an item, without removals and without ``ts_hash``."""

    components: Dict[str, Any] = dict(declaration.components)

    _add_effects(components, declaration)

    # Traits.
    if "food" in components:
        components.setdefault("consumable", {})
    if "max_damage" in components or "equippable" in components:
        components.setdefault("max_stack_size", 1)

    # Defaults.
    components.setdefault("max_stack_size", DEFAULT_MAX_STACK_SIZE)
    components.setdefault("item_name", title_case(item_id))
    components.setdefault("rarity", "common")

    # Core.
    custom_data = dict(components.get("custom_data", {}))
    custom_data["ts_name"] = item_id
    components["custom_data"] = custom_data
    components["custom_model_data"] = {"strings": [f"tasty_supplies/{item_id}"]}

    return components


def _add_effects(components: Dict[str, Any], declaration: Declaration) -> None:
    entries = list(declaration.consume_effects)

    if declaration.apply_effects:
        # Effects sharing a probability fit in a single entry.
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


def with_removals(
    components: Dict[str, Any], extra: Iterable[str] = ()
) -> Dict[str, Any]:
    """Add component removals, which a patch accepts but a predicate does not."""

    patch = dict(components)
    for name in (*DISABLED_COMPONENTS, *extra):
        patch[f"!minecraft:{name.removeprefix('minecraft:')}"] = {}
    return patch
