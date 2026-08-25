"""Items and recipes of the pack, one package per category.

Categories are listed in the order the recipe book shows them.
"""

import importlib
import pkgutil
from typing import Iterable

CATEGORIES = [
    "ingredients",
    "sweets",
    "drinks",
    "meals",
    "tools",
    "equipment",
    "workstations",
    "misc",
]


def discover(package: str, paths: Iterable[str]) -> None:
    """Import every module of a category package, in alphabetical order."""

    for module in sorted(info.name for info in pkgutil.iter_modules(paths)):
        importlib.import_module(f"{package}.{module}")
