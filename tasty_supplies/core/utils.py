from typing import Any, Dict, List


def to_absolute_path(item: str) -> str:
    """Convert a relative Minecraft item path to an absolute namespaced path."""

    if ":" in item:
        return item
    prefix = "#" if item.startswith("#") else ""
    clean_item = item.removeprefix("#")
    return f"{prefix}minecraft:{clean_item}"


def ensure_namespace(value: str, namespace: str, *, allow_tags: bool = True) -> str:
    """Ensure that an identifier is namespaced with the provided namespace."""

    if allow_tags and value.startswith("#"):
        tag_body = value[1:]
        return f"#{tag_body}" if ":" in tag_body else f"#{namespace}:{tag_body}"

    if value.startswith("#") and not allow_tags:
        raise ValueError("Namespaced identifiers cannot be tags in this context")

    if ":" in value:
        return value

    return f"{namespace}:{value}"


def remove_minecraft_namespace(data: Any) -> Any:
    """Remove 'minecraft:' prefix from component keys.

    Args:
        data: The data structure to process (dict, list, or primitive)

    Returns:
        Data with minecraft namespace removed from keys
    """
    if isinstance(data, dict):
        return {
            key.replace("minecraft:", ""): remove_minecraft_namespace(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [remove_minecraft_namespace(item) for item in data]
    else:
        return data


def to_snbt(data: Any) -> str:
    """Convert Python data to SNBT (Stringified NBT) format for Minecraft commands.

    Args:
        data: The data to convert (dict, list, string, bool, number)

    Returns:
        SNBT formatted string
    """
    if isinstance(data, dict):
        items: List[str] = [f"{key}:{to_snbt(value)}" for key, value in data.items()]
        return "{" + ",".join(items) + "}"
    elif isinstance(data, list):
        items: List[str] = [to_snbt(item) for item in data]
        return "[" + ",".join(items) + "]"
    elif isinstance(data, str):
        # Escape quotes in strings
        return '"' + data.replace('"', '\\"') + '"'
    elif isinstance(data, bool):
        return "true" if data else "false"
    elif isinstance(data, (int, float)):
        return str(data)
    else:
        return str(data)


def to_item_repr(item) -> str:
    """Return the item representation for Minecraft commands.

    Args:
        item: The Item instance
    Returns:
        <base_item>[<snbt_components>]
    """

    item_data: Dict[str, Any] = item.to_result()
    base_item: str = item_data["id"]
    components: Dict[str, Any] = item_data.get("components", {})
    components = remove_minecraft_namespace(components)

    # Generate SNBT for components
    snbt_components: str
    if components:
        component_items: List[str] = [
            f"{key}={to_snbt(value)}" for key, value in components.items()
        ]
        snbt_components = ",".join(component_items)
    else:
        snbt_components = ""

    result: str = f"{base_item}[{snbt_components}]"

    return result
