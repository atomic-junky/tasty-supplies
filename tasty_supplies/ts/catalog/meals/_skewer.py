from typing import List

from ts import Item, Shaped, remainder


@remainder("stick")
class Skewer(Item, abstract=True):
    """Two different things on a stick, craftable in either order."""

    top: str
    bottom: str

    def recipes(self) -> List:
        key = {"t": self.top, "b": self.bottom, "s": "stick"}
        return [
            Shaped(pattern=["t", "b", "s"], key=key),
            Shaped(id=f"{self.id}_reversed", pattern=["b", "t", "s"], key=key),
            *super().recipes(),
        ]
