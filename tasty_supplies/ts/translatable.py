from dataclasses import dataclass, field
from typing import List, Optional


_translatables: List[Translatable] = []


class Translatable(dict):
    def __init__(self, key: str, default: str, with_args: Optional[List[str]] = None, **kwargs) -> "Translatable":
        self.key = key
        self.default = default
        self.with_args = with_args or []
        self.kwargs = kwargs
        super().__init__(self.to_component())

        global _translatables
        _translatables.append(self)

    def to_component(self) -> dict:
        result = {"type": "translatable", "translate": self.key, "fallback": self.default}
        result.update(self.kwargs)
        if self.with_args:
            result["with"] = self.with_args

        return result