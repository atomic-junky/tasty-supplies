"""Conversions between Python values and Minecraft notations."""

import re
from typing import Any, Dict, List


def to_absolute_path(item: str) -> str:
    """Namespace a Minecraft identifier, preserving the ``#`` of tags."""

    if ":" in item:
        return item
    prefix = "#" if item.startswith("#") else ""
    return f"{prefix}minecraft:{item.removeprefix('#')}"


def snake_case(name: str) -> str:
    """``ApplePieSlice`` -> ``apple_pie_slice``."""

    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def title_case(item_id: str) -> str:
    """``apple_pie`` -> ``Apple Pie``."""

    return " ".join(word.capitalize() for word in item_id.split("_"))


def remove_minecraft_namespace(data: Any) -> Any:
    if isinstance(data, dict):
        return {
            key.replace("minecraft:", ""): remove_minecraft_namespace(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [remove_minecraft_namespace(item) for item in data]
    return data


#: Characters a compound key may use unquoted; a namespaced key needs quotes.
_BARE_KEY = re.compile(r"[A-Za-z0-9_.+-]+")


def to_snbt(data: Any) -> str:
    """Serialize a Python value to SNBT, for Minecraft commands."""

    if isinstance(data, dict):
        items: List[str] = [
            f"{_snbt_key(key)}:{to_snbt(value)}" for key, value in data.items()
        ]
        return "{" + ",".join(items) + "}"
    if isinstance(data, list):
        return "[" + ",".join(to_snbt(item) for item in data) + "]"
    if isinstance(data, str):
        return '"' + data.replace('"', '\\"') + '"'
    if isinstance(data, bool):
        return "true" if data else "false"
    return str(data)


def _snbt_key(key: str) -> str:
    return key if _BARE_KEY.fullmatch(key) else to_snbt(key)


def components_to_snbt(components: Dict[str, Any]) -> str:
    """Serialize components for the ``item[...]`` syntax of commands.

    A key prefixed with ``!`` is a removal, written alone without a value.
    """

    parts: List[str] = []
    for key, value in remove_minecraft_namespace(components).items():
        parts.append(key if key.startswith("!") else f"{key}={to_snbt(value)}")

    return ",".join(parts).translate(str.maketrans({"\n": r"\n", "\r": r"\r"}))
