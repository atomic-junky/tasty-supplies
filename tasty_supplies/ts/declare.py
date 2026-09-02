"""The decorators used to declare an item or a recipe.

``component`` covers every vanilla component; the others are sugar producing
the same contribution, and each one forwards extra keyword arguments to the
component it writes.

Anything describing a recipe (``count``, ``time``, ``xp``, ``id``) belongs to
its decorator, so two recipes on one class can differ.
"""

from typing import Any, Callable, Dict, List, Optional

from . import declaration as kinds
from .components import RARITIES
from .recipe import Brewing, BrewingRef, Cooked, Cut, Ref, Shaped, Shapeless, Smithing
from .utils import to_absolute_path

Decorator = Callable[[type], type]


def _contribute(kind: str, payload: Any) -> Decorator:
    def apply(cls: type) -> type:
        cls.contribute(kind, payload)
        return cls

    return apply


def component(**raw: Any) -> Decorator:
    """Set raw components, e.g. ``@component(use_cooldown={"seconds": 2.0})``."""

    return _contribute(kinds.COMPONENT, raw)


def food(nutrition: float, saturation: float, **extra: Any) -> Decorator:
    """Make the item edible."""

    return component(food={"nutrition": nutrition, "saturation": saturation, **extra})


def stack(size: int) -> Decorator:
    """Override the maximum stack size (64 by default)."""

    return component(max_stack_size=size)


def rarity(value: str) -> Decorator:
    """Set the item rarity, which colours its name."""

    if value not in RARITIES:
        raise ValueError(f"Unknown rarity {value!r}, expected one of {RARITIES}.")
    return component(rarity=value)


def remainder(item: str) -> Decorator:
    """Item left in the inventory once this one is used up."""

    return component(use_remainder={"id": to_absolute_path(item)})


def cooldown(seconds: float, group: Optional[str] = None) -> Decorator:
    """Cooldown applied after use, optionally shared across a group of items."""

    options: Dict[str, Any] = {"seconds": seconds}
    if group:
        options["cooldown_group"] = group
    return component(use_cooldown=options)


def apply_effect(
    effect_id: str,
    duration: int = 0,
    amplifier: int = 0,
    *,
    probability: Optional[float] = None,
    **extra: Any,
) -> Decorator:
    """Apply a status effect on consumption.

    Several ``apply_effect`` merge into a single entry; a different
    ``probability`` starts a new one. ``extra`` goes on the effect instance.
    """

    effect = {
        "id": to_absolute_path(effect_id),
        "duration": duration,
        "amplifier": amplifier,
        **extra,
    }
    return _contribute(kinds.APPLY_EFFECT, (probability, effect))


def consume_effect(effect_type: str, **params: Any) -> Decorator:
    """Any consumption effect: ``teleport_randomly``, ``clear_all_effects``,
    ``remove_effects``, ``play_sound``, ``apply_effects``."""

    return _contribute(kinds.CONSUME_EFFECT, {"type": effect_type, **params})


def potion_effect(
    effect_id: str, duration: int = 0, amplifier: int = 0, **extra: Any
) -> Decorator:
    """Add an effect to a drink, through ``potion_contents``."""

    effect = {
        "id": to_absolute_path(effect_id),
        "duration": duration,
        "amplifier": amplifier,
        **extra,
    }
    return _contribute(kinds.POTION_EFFECT, effect)


def disable(*names: str) -> Decorator:
    """Drop vanilla components from this item only.

    ``components.DISABLED_COMPONENTS`` holds the ones dropped everywhere.
    """

    return _contribute(kinds.DISABLE, list(names))


def shaped(
    pattern: List[str],
    key: Optional[Dict[str, Ref]] = None,
    *,
    count: int = 1,
    id: str = "",
    **keys: Ref,
) -> Decorator:
    """Crafting recipe with a layout.

    Pattern characters are passed as keyword arguments; ``key`` takes an
    explicit mapping instead. ``id`` names the recipe file, which otherwise
    takes the name of the item and a number.
    """

    return _contribute(
        kinds.RECIPE,
        Shaped(id=id, count=count, pattern=pattern, key={**(key or {}), **keys}),
    )


def shapeless(*items: Ref, count: int = 1, id: str = "") -> Decorator:
    """Crafting recipe with no layout."""

    return _contribute(kinds.RECIPE, Shapeless(id=id, count=count, items=list(items)))


def brew(input: BrewingRef, reagent: BrewingRef, output: Ref) -> Decorator:
    """Brewing stand recipe."""

    input_potion: Optional[str] = input[1] if isinstance(input, tuple) else None
    reagent_potion: Optional[str] = reagent[1] if isinstance(reagent, tuple) else None

    return _contribute(
        kinds.RECIPE,
        Brewing(input=input, reagent=reagent, result=output, input_potion=input_potion, reagent_potion=reagent_potion)
    )


def cooked(
    ingredient: Ref, *, time: int = 200, xp: float = 0.1, count: int = 1, id: str = ""
) -> Decorator:
    """Furnace, smoker and campfire recipes at once. ``time`` is the base time."""

    return _contribute(
        kinds.RECIPE,
        Cooked(id=id, count=count, ingredient=ingredient, time=time, xp=xp),
    )


def cut(ingredient: Ref, *, count: int = 1, id: str = "") -> Decorator:
    """Cutting board recipe."""

    return _contribute(kinds.RECIPE, Cut(id=id, count=count, ingredient=ingredient))


def smithing(
    base: Ref,
    addition: Ref,
    *,
    template: Ref = "netherite_upgrade_smithing_template",
    count: int = 1,
    id: str = "",
) -> Decorator:
    """Smithing table upgrade."""

    return _contribute(
        kinds.RECIPE,
        Smithing(id=id, count=count, template=template, base=base, addition=addition),
    )
