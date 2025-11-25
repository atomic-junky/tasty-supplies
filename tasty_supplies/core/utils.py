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
