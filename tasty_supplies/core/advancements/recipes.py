"""Helpers for recipe-related advancement wiring.

This module provides utilities to extract recipe ids from advancement criteria
and to build simple rewards payloads. It intentionally keeps logic minimal and
lets callers resolve recipe existence using the Bucket where appropriate.
"""

from __future__ import annotations

from typing import Dict, List, Any

from ..utils import ensure_namespace
from ..constants import TASTY_SUPPLIES_NAMESPACE


def extract_recipe_ids_from_criteria(criteria: Dict[str, Any]) -> List[str]:
    """Scan an advancement `criteria` mapping and return all referenced
    recipe ids from `minecraft:recipe_crafted` triggers.

    The returned ids are normalized (namespaced) with the Tasty Supplies
    namespace when missing.
    """
    ids: List[str] = []

    for name, entry in criteria.items():
        if not isinstance(entry, dict):
            continue

        trigger = entry.get("trigger")
        if trigger != "minecraft:recipe_crafted":
            continue

        conditions = entry.get("conditions") or {}
        recipe_id = conditions.get("recipe_id")
        if not recipe_id:
            continue

        normalized = ensure_namespace(
            str(recipe_id), TASTY_SUPPLIES_NAMESPACE, allow_tags=False
        )
        ids.append(normalized)

    return ids
