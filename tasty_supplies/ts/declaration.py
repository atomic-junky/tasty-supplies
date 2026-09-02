"""The declaration machinery shared by items and standalone recipes.

Each decorator drops a contribution on the class it decorates. Contributions
are then merged along the MRO, from the base class down to the concrete one, so
an abstract family can set values that a subclass overrides.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Type

from .utils import snake_case

#: Every concrete declared class, in definition order.
REGISTERED: List[Type["Declarable"]] = []

COMPONENT = "component"
APPLY_EFFECT = "apply_effect"
CONSUME_EFFECT = "consume_effect"
POTION_EFFECT = "potion_effect"
RECIPE = "recipe"
DISABLE = "disable"

#: Contributions that pile up instead of replacing one another.
ACCUMULATING = (APPLY_EFFECT, CONSUME_EFFECT, POTION_EFFECT, RECIPE)


@dataclass
class Declaration:
    """The merged contributions of a class and its ancestors."""

    components: Dict[str, Any] = field(default_factory=dict)
    apply_effects: List[tuple] = field(default_factory=list)
    consume_effects: List[dict] = field(default_factory=list)
    potion_effects: List[dict] = field(default_factory=list)
    recipes: List[Any] = field(default_factory=list)
    disabled: List[str] = field(default_factory=list)


class Declarable:
    """Base class for everything the catalog declares."""

    abstract: bool = True
    id: str = ""

    __own_contributions__: List[Tuple[str, Any]] = []

    def __init_subclass__(cls, abstract: bool = False, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        cls.abstract = abstract
        # Local to this class, so a subclass never appends to its parent list.
        cls.__own_contributions__ = []

        if "id" not in cls.__dict__:
            cls.id = snake_case(cls.__name__)

        if not abstract:
            REGISTERED.append(cls)

    @classmethod
    def contribute(cls, kind: str, payload: Any) -> None:
        """Record a contribution, called by the decorators."""

        cls.__own_contributions__.append((kind, payload))

    @classmethod
    def declaration(cls) -> Declaration:
        """Merge contributions, from the base class down to this one."""

        merged = Declaration()

        for ancestor in reversed(cls.__mro__):
            own = ancestor.__dict__.get("__own_contributions__", [])

            for kind, payload in own:
                if kind == COMPONENT:
                    merged.components.update(payload)
                elif kind == DISABLE:
                    merged.disabled.extend(payload)
                elif kind not in ACCUMULATING:
                    raise ValueError(f"Unknown contribution: {kind!r}")

            for kind, payload in reversed(own):
                if kind == APPLY_EFFECT:
                    merged.apply_effects.append(payload)
                elif kind == CONSUME_EFFECT:
                    merged.consume_effects.append(payload)
                elif kind == POTION_EFFECT:
                    merged.potion_effects.append(payload)
                elif kind == RECIPE:
                    merged.recipes.append(payload)

        return merged
