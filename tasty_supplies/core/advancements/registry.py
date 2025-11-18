"""Advancement registration routines for the datapack generator."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, Optional, List

import json
import os

from ..bucket import Bucket
from ..constants import (
    COMPONENT_CUSTOM_MODEL_DATA,
    MINECRAFT_NAMESPACE,
    TASTY_SUPPLIES_NAMESPACE,
)
from ..logger import log
from ..models.advancement import (
    Advancement,
    AdvancementIcon,
    AdvancementCriteria,
    AdvancementRewards,
    ADVANCEMENT_TYPE,
)
from ..models.item import Item
from ..utils import ensure_namespace


def _recipe_criteria(recipe_id: str) -> AdvancementCriteria:
    return AdvancementCriteria(
        trigger="minecraft:recipe_crafted",
        conditions={
            "recipe_id": ensure_namespace(
                recipe_id,
                TASTY_SUPPLIES_NAMESPACE,
                allow_tags=False,
            ),
        },
    )


def _item_condition(
    item: Item, extra_components: Optional[Dict[str, object]] = None
) -> Dict[str, object]:
    components = {
        f"{MINECRAFT_NAMESPACE}:{COMPONENT_CUSTOM_MODEL_DATA}": {
            "strings": [f"{TASTY_SUPPLIES_NAMESPACE}/{item.name}"]
        }
    }
    if extra_components:
        components.update(deepcopy(extra_components))
    return {
        "items": [f"{MINECRAFT_NAMESPACE}:{item.base_item}"],
        "components": components,
    }


def _consume_item_criteria(item: Item) -> AdvancementCriteria:
    return AdvancementCriteria(
        trigger="minecraft:consume_item",
        conditions={
            "item": _item_condition(item, item.components if getattr(item, 'components', None) else None),
        },
    )


def _inventory_item_criteria(
    item: Item, extra_components: Optional[Dict[str, object]] = None
) -> AdvancementCriteria:
    return AdvancementCriteria(
        trigger="minecraft:inventory_changed",
        conditions={
            "items": [
                _item_condition(item, extra_components if extra_components is not None else (item.components if getattr(item, 'components', None) else None)),
            ],
        },
    )


def _inventory_vanilla_item_criteria(item_id: str) -> AdvancementCriteria:
    return AdvancementCriteria(
        trigger="minecraft:inventory_changed",
        conditions={
            "items": [
                {
                    "items": [
                        ensure_namespace(
                            item_id,
                            MINECRAFT_NAMESPACE,
                        )
                    ]
                }
            ]
        },
    )


def _require_item(bucket: Bucket, item_name: str) -> Item:
    item = bucket.get(item_name)
    if not item:
        raise ValueError(
            f"Missing item '{item_name}' required for advancement generation."
        )
    return item


def _optional_components(
    item: Item, keys: Iterable[str]
) -> Optional[Dict[str, object]]:
    collected: Dict[str, object] = {}
    for key in keys:
        if key in item.components:
            collected[key] = deepcopy(item.components[key])
    return collected or None


def _item_predicate_from_item(item: Item) -> Dict[str, object]:
    """Return a Minecraft item predicate dict for the given Item, including components."""
    return _item_condition(item, item.components if getattr(item, "components", None) else None)


def _item_predicate_from_name(bucket: Bucket, name: str) -> Dict[str, object]:
    """Lookup an item by name from the bucket and return its item predicate."""
    itm = _require_item(bucket, name)
    return _item_predicate_from_item(itm)


def _inventory_criterion_from_names(bucket: Bucket, names: Iterable[str]) -> AdvancementCriteria:
    """Build a single `minecraft:inventory_changed` criterion matching any of the provided item names.

    Each name is resolved via `_require_item` so the predicate includes the exact components.
    """
    predicates = [_item_predicate_from_name(bucket, n) for n in names]
    return AdvancementCriteria(trigger="minecraft:inventory_changed", conditions={"items": predicates})


def _resolve_placeholders(obj: Any, bucket: Bucket) -> Any:
    """Recursively resolve placeholder strings in the provided object.

    Supported placeholder forms (as complete string values):
      - `$name` -> returns an item-predicate dict for the bucket item `name`
      - `$name.id` or `$name.name` -> returns the namespaced item id string `tasty_supplies:name`
      - `$name.icon` -> returns an icon dict compatible with AdvancementIcon (id + components)
    """
    # Primitive types
    if isinstance(obj, str):
        if not obj.startswith("$"):
            return obj
        token = obj[1:]
        if "." in token:
            name, attr = token.split(".", 1)
        else:
            name, attr = token, None

        itm = bucket.get(name)
        if not itm:
            log.warning(f"Template references unknown item '{name}'")
            return obj

        if attr is None:
            return _item_predicate_from_item(itm)

        # explicit predicate request
        if attr in ("predicate", "item_predicate"):
            return _item_predicate_from_item(itm)

        if attr in ("id", "name", "namespaced"):
            return f"{TASTY_SUPPLIES_NAMESPACE}:{name}"

        if attr in ("icon", "icon_dict"):
            icon = {"id": f"{MINECRAFT_NAMESPACE}:{itm.base_item}"}
            if getattr(itm, "components", None):
                icon["components"] = deepcopy(itm.components)
            return icon

        # Unknown attribute -> return original string
        return obj

    # Lists
    if isinstance(obj, list):
        return [_resolve_placeholders(v, bucket) for v in obj]

    # Dicts
    if isinstance(obj, dict):
        # Support a JSON-native placeholder object like {"$ref": "apple_pie.predicate"}
        if len(obj) == 1:
            k = next(iter(obj.keys()))
            if isinstance(k, str) and k.startswith("$"):
                v = obj[k]
                # allow either "$ref": "name.attr" or "$predicate": "name"
                if isinstance(v, str):
                    token = v if not v.startswith("$") else v[1:]
                    if "." in token:
                        name, attr = token.split(".", 1)
                    else:
                        name, attr = token, None

                    itm = bucket.get(name)
                    if not itm:
                        log.warning(f"Template references unknown item '{name}'")
                        return obj

                    if attr is None:
                        return _item_predicate_from_item(itm)

                    if attr in ("predicate", "item_predicate"):
                        return _item_predicate_from_item(itm)

                    if attr in ("id", "name", "namespaced"):
                        return f"{TASTY_SUPPLIES_NAMESPACE}:{name}"

                    if attr in ("icon", "icon_dict"):
                        icon = {"id": f"{MINECRAFT_NAMESPACE}:{itm.base_item}"}
                        if getattr(itm, "components", None):
                            icon["components"] = deepcopy(itm.components)
                        return icon

                    return obj

        out: dict = {}
        for k, v in obj.items():
            out[k] = _resolve_placeholders(v, bucket)
        return out

    # Other types pass-through
    return obj


def _template_directories() -> List[str]:
    """Directories that may contain advancement templates."""

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    candidates = [
        os.path.join(
            base_dir,
            "src",
            "data",
            TASTY_SUPPLIES_NAMESPACE,
            "advancements",
        ),
        os.path.join(base_dir, "advancements"),
    ]
    return [path for path in candidates if os.path.isdir(path)]


def _namespace_from_templates_dir(path: str) -> str:
    parts = os.path.normpath(path).split(os.sep)
    if "data" in parts:
        idx = parts.index("data")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return TASTY_SUPPLIES_NAMESPACE


def _strip_namespace_prefix(identifier: str, namespace: str) -> str:
    """Remove redundant "namespace/" prefixes from a resource path."""

    prefix = f"{namespace}/"
    if identifier.startswith(prefix):
        return identifier[len(prefix) :]
    return identifier


def _normalize_advancement_path(raw_id: str, namespace: str) -> str:
    """Coerce advancement identifiers to a path relative to the namespace."""

    if ":" in raw_id:
        ns, path = raw_id.split(":", 1)
        if ns != namespace:
            raise ValueError(
                f"Unsupported namespace '{ns}' for advancement template (expected '{namespace}')"
            )
        raw_id = path

    return _strip_namespace_prefix(raw_id, namespace)


def _normalize_parent_reference(parent: str, namespace: str) -> str:
    """Normalize parent references to avoid duplicated namespace segments."""

    target_namespace = namespace
    path = parent

    if ":" in parent:
        target_namespace, path = parent.split(":", 1)

    if target_namespace == namespace:
        return _strip_namespace_prefix(path, namespace)

    return f"{target_namespace}:{_strip_namespace_prefix(path, target_namespace)}"


def _load_advancement_templates(bucket: Bucket) -> bool:
    """Load advancement templates (if present)."""

    template_dirs = _template_directories()
    loaded = False

    for templates_dir in template_dirs:
        namespace = _namespace_from_templates_dir(templates_dir)
        for root_dir, _, files in os.walk(templates_dir):
            for fname in files:
                if not fname.endswith(".json"):
                    continue
                path = os.path.join(root_dir, fname)
                try:
                    with open(path, "r", encoding="utf-8") as fh:
                        data = json.load(fh)
                except Exception as exc:
                    log.warning(
                        f"Failed to load advancement template {os.path.relpath(path, templates_dir)}: {exc}"
                    )
                    continue

                resolved = _resolve_placeholders(data, bucket)

                adv_id_raw = resolved.get("advancement_id") or resolved.get("id")
                if not adv_id_raw:
                    rel = os.path.splitext(
                        os.path.relpath(path, os.path.join(templates_dir))
                    )[0].replace(os.sep, "/")
                    ns_prefix = f"{namespace}/"
                    if rel.startswith(ns_prefix):
                        rel = rel[len(ns_prefix) :]
                    adv_id = rel
                else:
                    try:
                        adv_id = _normalize_advancement_path(adv_id_raw, namespace)
                    except ValueError as exc:
                        log.warning(
                            "Skipping advancement template %s: %s",
                            os.path.relpath(path, templates_dir),
                            exc,
                        )
                        continue

                if "id" in resolved:
                    log.debug(
                        "Template %s still declares an 'id' field; prefer `advancement_id` or rely on file path.",
                        os.path.relpath(path, templates_dir),
                    )

                display_data = resolved.get("display")
                if not isinstance(display_data, dict):
                    display_data = {}

                title = resolved.get("title", display_data.get("title", ""))
                description = resolved.get(
                    "description", display_data.get("description", "")
                )
                icon = resolved.get("icon") or display_data.get("icon")
                criteria = resolved.get("criteria", {})
                parent = resolved.get("parent")
                if isinstance(parent, str):
                    parent = _normalize_parent_reference(parent, namespace)
                requirements = resolved.get("requirements")
                adv_type = resolved.get("type") or display_data.get("frame")
                background = resolved.get("background") or display_data.get(
                    "background"
                )
                show_toast = resolved.get(
                    "show_toast", display_data.get("show_toast", True)
                )
                announce = resolved.get(
                    "announce_to_chat", display_data.get("announce_to_chat", False)
                )
                hidden = resolved.get("hidden", display_data.get("hidden", False))
                telemetry = resolved.get(
                    "sends_telemetry_event",
                    display_data.get("sends_telemetry_event", True),
                )

                rewards_payload = resolved.get("rewards")
                rewards = None
                if isinstance(rewards_payload, dict):
                    rewards = AdvancementRewards(
                        experience=rewards_payload.get("experience", 0),
                        recipes=rewards_payload.get("recipes"),
                        loot=rewards_payload.get("loot"),
                        function=rewards_payload.get("function"),
                    )

                adv_type_enum = ADVANCEMENT_TYPE.TASK
                if isinstance(adv_type, str):
                    try:
                        adv_type_enum = ADVANCEMENT_TYPE(adv_type)
                    except ValueError:
                        pass

                handled_display_keys = {
                    "title",
                    "description",
                    "icon",
                    "frame",
                    "background",
                    "hidden",
                    "show_toast",
                    "announce_to_chat",
                    "sends_telemetry_event",
                }
                display_extras = {
                    key: value
                    for key, value in display_data.items()
                    if key not in handled_display_keys
                }

                try:
                    adv = Advancement(
                        advancement_id=adv_id,
                        title=title,
                        description=description,
                        icon=icon if icon is not None else "minecraft:stone",
                        criteria=criteria,
                        parent=parent,
                        advancement_type=adv_type_enum,
                        requirements=requirements,
                        rewards=rewards,
                        background=background,
                        show_toast=show_toast,
                        announce_to_chat=announce,
                        hidden=hidden,
                        sends_telemetry_event=telemetry,
                        **display_extras,
                    )
                except Exception as exc:
                    log.warning(
                        f"Failed to construct Advancement from template {os.path.relpath(path, templates_dir)}: {exc}"
                    )
                    continue

                bucket.add_advancement(adv, category=resolved.get("category"))
                loaded = True

    return loaded


def register_advancements(bucket: Bucket) -> None:
    """Register all advancements using the provided bucket content."""

    log.debug("Registering advancements via bucket")

    if _load_advancement_templates(bucket):
        return

    raise RuntimeError(
        "No advancement templates were loaded. Ensure JSON files exist under "
        "src/data/tasty_supplies/advancements or tasty_supplies/advancements."
    )
