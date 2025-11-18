"""Utility to convert generated advancements into placeholder templates."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
BUILD_ADV_DIR = (
    ROOT
    / "tasty_supplies"
    / "build"
    / "Tasty Supplies - Data Pack"
    / "data"
    / "tasty_supplies"
    / "advancement"
)
TEMPLATE_DIR = (
    ROOT
    / "tasty_supplies"
    / "src"
    / "data"
    / "tasty_supplies"
    / "advancements"
)
CUSTOM_PREFIX = "tasty_supplies/"


def extract_item_name(components: Any) -> str | None:
    if not isinstance(components, dict):
        return None
    for key, value in components.items():
        if not key.endswith("custom_model_data"):
            continue
        if not isinstance(value, dict):
            continue
        strings = value.get("strings")
        if not isinstance(strings, list) or len(strings) != 1:
            continue
        entry = strings[0]
        if isinstance(entry, str) and entry.startswith(CUSTOM_PREFIX):
            return entry[len(CUSTOM_PREFIX) :]
    return None


def transform(node: Any) -> Any:
    if isinstance(node, dict):
        item_name = extract_item_name(node.get("components"))
        if item_name:
            if "id" in node:
                return f"${item_name}.icon"
            return f"${item_name}.predicate"
        return {key: transform(value) for key, value in node.items()}

    if isinstance(node, list):
        return [transform(value) for value in node]

    return node


def derive_advancement_id(json_path: Path, root_dir: Path) -> str:
    relative = json_path.relative_to(root_dir)
    without_suffix = relative.with_suffix("")
    namespace = without_suffix.parts[0]
    path_inside = "/".join(without_suffix.parts[1:])
    return f"{namespace}/{path_inside}" if path_inside else namespace


def main() -> None:
    if not BUILD_ADV_DIR.exists():
        raise SystemExit(f"Build directory not found: {BUILD_ADV_DIR}")

    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

    for json_path in BUILD_ADV_DIR.rglob("*.json"):
        with json_path.open("r", encoding="utf-8") as fh:
            data: Dict[str, Any] = json.load(fh)

        transformed = transform(data)

        target_path = TEMPLATE_DIR / json_path.relative_to(BUILD_ADV_DIR)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open("w", encoding="utf-8") as fh:
            json.dump(transformed, fh, indent=2)
            fh.write("\n")

        print(f"Wrote template: {target_path.relative_to(TEMPLATE_DIR)}")


if __name__ == "__main__":
    main()
