from typing import Any, Dict, List


def to_absolute_path(item: str) -> str:
    """Convert a relative Minecraft item path to an absolute namespaced path.

    Args:
        item: Item identifier (e.g., "apple", "#planks", "minecraft:stone")

    Returns:
        Absolute namespaced path (e.g., "minecraft:apple", "#minecraft:planks")
    """
    if ":" in item:
        return item
    prefix = "#" if item.startswith("#") else ""
    clean_item = item.removeprefix("#")
    return f"{prefix}minecraft:{clean_item}"


def remove_minecraft_namespace(data: Any) -> Any:
    """Remove the ``minecraft:`` prefix from component keys recursively."""

    if isinstance(data, dict):
        return {
            key.replace("minecraft:", ""): remove_minecraft_namespace(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [remove_minecraft_namespace(item) for item in data]
    return data


def to_snbt(data: Any) -> str:
    """Convert Python data structures to SNBT format."""

    if isinstance(data, dict):
        items: List[str] = [f"{key}:{to_snbt(value)}" for key, value in data.items()]
        return "{" + ",".join(items) + "}"
    if isinstance(data, list):
        items = [to_snbt(item) for item in data]
        return "[" + ",".join(items) + "]"
    if isinstance(data, str):
        return '"' + data.replace('"', '\\"') + '"'
    if isinstance(data, bool):
        return "true" if data else "false"
    if isinstance(data, (int, float)):
        return str(data)
    return str(data)
