"""Which texture is drawn for an ingredient of the recipe book.

A vanilla item is not always drawn with ``item/<id>.png``: a mushroom uses a
block texture, and a tag has to pick one of its members. Both are found by
following what the game itself follows, the item model and the item tag.

An item whose model is not a flat sprite, a block, has no texture to reuse: it
is rendered the way the inventory draws it, through model_resolver.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from beet import Context, DataPack, ResourcePack
from beet.contrib.vanilla import Vanilla
from PIL import Image

from ..item import Item
from ..recipe import Ref
from ..utils import to_absolute_path

logger = logging.getLogger(__name__)

TEXTURE_KEYS = ("layer0", "all", "texture", "side", "particle", "top")
FLAT_MODELS = ("item/generated", "item/handheld")
ICON_SIZE = 16
MAX_DEPTH = 10


class Textures:
    """Resolves an ingredient to the texture drawn for it."""

    def __init__(self, ctx: Context) -> None:
        vanilla = ctx.inject(Vanilla)
        self.ctx = ctx
        self.assets: ResourcePack = vanilla.assets
        self.data: DataPack = vanilla.data
        self.pack = ctx.assets
        self.tags = ctx.data
        self.pending: Dict[str, str] = {}

    def of(self, ref: Ref) -> Optional[str]:
        if isinstance(ref, Item):
            return f"{ref.texture_path}.png"
        if not isinstance(ref, str):
            return None

        identifier = to_absolute_path(ref)
        if identifier.startswith("#"):
            identifier = self._first_member(identifier[1:])
            if identifier is None:
                return None

        return self._from_item_model(identifier)

    def _first_member(self, tag: str, depth: int = 0) -> Optional[str]:
        """The item a tag is drawn with, the first one it holds."""

        values = self.tags.item_tags.get(tag) or self.data.item_tags.get(tag)
        if values is None or depth > MAX_DEPTH:
            return None

        for value in values.data.get("values", []):
            entry = value["id"] if isinstance(value, dict) else value
            if entry.startswith("#"):
                entry = self._first_member(entry[1:], depth + 1)
            if entry:
                return entry

        return None

    def _from_item_model(self, identifier: str) -> Optional[str]:
        definition = self.assets.item_models.get(identifier)
        if definition is None:
            return None

        path = _model_path(definition.data.get("model"))
        if path is None:
            return None

        chain = self._chain(path)
        if not _is_flat(chain):
            return self._render(identifier)

        textures = _textures_of(chain)
        for key in (*TEXTURE_KEYS, *sorted(textures)):
            if key in textures:
                return f"{to_absolute_path(textures[key])}.png"

        return None

    def _chain(self, path: str) -> List[Tuple[str, dict]]:
        """A model and the parents it inherits from."""

        chain: List[Tuple[str, dict]] = []
        for _ in range(MAX_DEPTH):
            path = to_absolute_path(path)
            model = self.assets.models.get(path)
            if model is None:
                break
            chain.append((path, model.data))
            path = model.data.get("parent")
            if not path:
                break

        return chain

    def _render(self, identifier: str) -> str:
        name = identifier.removeprefix("minecraft:").replace("/", "_")
        path = f"tasty_supplies:recipe_book/render/{name}"
        self.pending[identifier] = path
        return f"{path}.png"

    def render_pending(self) -> None:
        """Draw the models that have no flat texture to reuse."""

        if not self.pending:
            return

        from model_resolver import Render
        from model_resolver.item_model.item import Item as RenderTarget

        options = {
            **self.ctx.meta.get("model_resolver", {}),
            "minecraft_version": self._release(),
        }

        with self.ctx.override(model_resolver=options):
            render = Render(self.ctx)
            for identifier, path in self.pending.items():
                render.add_item_task(RenderTarget(id=identifier), path_ctx=path)
            render.run()

        for identifier, path in self.pending.items():
            texture = self.pack.textures.get(path)
            if texture is None:
                logger.warning("Could not render %r for the recipe book.", identifier)
                continue
            texture.image = texture.image.convert("RGBA").resize(
                (ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS
            )

        logger.info("Rendered %d models for the recipe book.", len(self.pending))
        self.pending.clear()

    def _release(self) -> str:
        vanilla = self.ctx.inject(Vanilla)
        release = vanilla.releases[vanilla.minecraft_version]
        return release.info.data["id"]

    def image(self, texture: str):
        path = texture.removesuffix(".png")
        pack = self.assets if path.startswith("minecraft:") else self.pack
        found = pack.textures.get(path)
        return getattr(found, "image", None) if found is not None else None

    def exists(self, texture: str) -> bool:
        return self.image(texture) is not None


def _model_path(model: Any) -> Optional[str]:
    """Walk an item model down to a plain model, taking its default branch."""

    if not isinstance(model, dict):
        return None
    if model.get("type") == "minecraft:model":
        return model.get("model")

    for key in ("fallback", "on_false", "on_true", "model"):
        found = _model_path(model.get(key))
        if found:
            return found

    for key in ("cases", "entries"):
        for case in model.get(key) or []:
            found = _model_path(case.get("model") if isinstance(case, dict) else None)
            if found:
                return found

    return None


def _is_flat(chain: List[Tuple[str, dict]]) -> bool:
    return any(path.removeprefix("minecraft:") in FLAT_MODELS for path, _ in chain)


def _textures_of(chain: List[Tuple[str, dict]]) -> Dict[str, str]:
    """The textures of a model, those of its parents included."""

    textures: Dict[str, str] = {}
    for _, data in chain:
        for key, value in data.get("textures", {}).items():
            textures.setdefault(key, value)

    return {
        key: textures.get(value[1:], value) if value.startswith("#") else value
        for key, value in textures.items()
    }
