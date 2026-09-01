"""What the JSON files of ``src/`` can call, through the Jinja renderer.

``items.<id>`` reaches an item of the catalog, and ``extend_loot_table`` adds
to a vanilla table. Only the files listed under ``render`` in ``beet.yml`` go
through Jinja.
"""

import json
from copy import deepcopy
from typing import Any, Dict, List, Optional

from beet import Context
from beet.contrib.vanilla import Vanilla

from .item import Item
from .registry import Registry


class UnknownItem(Exception):
    """Raised when a template asks for an item that does not exist.

    Neither an ``AttributeError`` nor a ``LookupError``, which Jinja swallows.
    """


class ItemLookup:
    """``items.apple_pie`` in a template."""

    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    def __getattr__(self, name: str) -> Item:
        if name.startswith("_"):
            raise AttributeError(name)
        item = self._registry.get(name)
        if item is None:
            raise UnknownItem(f"No item named {name!r} in the catalog.")
        return item

    def __getitem__(self, name: str) -> Item:
        return getattr(self, name)


def extend_loot_table(
    ctx: Context,
    path: str,
    *,
    pools: Optional[List[dict]] = None,
    entries: Optional[Dict[Any, list]] = None,
) -> str:
    """The vanilla loot table, plus our own pools and entries.

    ``pools`` are appended to the table, ``entries`` to the pool of the given
    index. The vanilla data is copied, since beet caches it.
    """

    vanilla = ctx.inject(Vanilla)
    table = deepcopy(vanilla.data.loot_tables[path].data)

    for index, added in (entries or {}).items():
        table["pools"][int(index)]["entries"].extend(added)

    if pools:
        table.setdefault("pools", []).extend(pools)

    return json.dumps(table)


def register(ctx: Context, registry: Registry) -> None:
    """Expose the catalog to the templates."""

    ctx.template.globals["items"] = ItemLookup(registry)
    ctx.template.globals["extend_loot_table"] = (
        lambda path, **kwargs: extend_loot_table(ctx, path, **kwargs)
    )
    # The tojson of Jinja escapes HTML, which a data pack has no use for.
    ctx.template.env.filters["tojson"] = json.dumps
