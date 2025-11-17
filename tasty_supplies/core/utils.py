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
