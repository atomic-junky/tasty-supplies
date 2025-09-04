def to_absolute_path(item: str) -> str:
    if ":" in item:
        return item
    return f"{"#" if item.startswith("#") else ""}minecraft:{item.removeprefix("#")}"
