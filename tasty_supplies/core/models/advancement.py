"""Advancement model used by the datapack generator."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from beet import Advancement as BeetAdvancement

from .context import TSContext
from .item import Item
from .recipe import Recipe
from ..constants import (
    COMPONENT_CUSTOM_MODEL_DATA,
    MINECRAFT_NAMESPACE,
    TASTY_SUPPLIES_NAMESPACE,
)
from ..logger import log
from ..utils import ensure_namespace

IconType = Union[str, Item, Dict[str, Any]]
PlayerPredicateType = Union[Dict[str, Any], List[Dict[str, Any]]]
CriteriaEntry = Union["AdvancementCriteria", Dict[str, Any]]
CriteriaMapping = Dict[str, CriteriaEntry]


class ADVANCEMENT_TYPE(Enum):
    """Available display frame types for advancements."""

    CHALLENGE = "challenge"
    GOAL = "goal"
    TASK = "task"


class AdvancementRequirements:
    """Utility container for describing completion requirements."""

    def __init__(self, requirements: Dict[str, Any]):
        self.requirements = requirements

    def __repr__(self) -> str:
        return f"AdvancementRequirements(requirements={self.requirements})"


class AdvancementIcon:
    """Icon definition supporting vanilla items, custom items, or raw dicts."""

    def __init__(
        self,
        icon: IconType,
        count: int = 1,
        components: Optional[Dict[str, Any]] = None,
        **extra_components: Any,
    ) -> None:
        self.icon = icon
        self.count = count
        merged_components: Dict[str, Any] = {}
        if components:
            merged_components.update(deepcopy(components))
        if extra_components:
            merged_components.update(deepcopy(extra_components))
        self.components = merged_components

    def to_json(self) -> Dict[str, Any]:
        if isinstance(self.icon, dict):
            icon_data = deepcopy(self.icon)
            if self.components:
                existing = deepcopy(icon_data.get("components", {}))
                existing.update(deepcopy(self.components))
                icon_data["components"] = existing
            if "count" not in icon_data and self.count != 1:
                icon_data["count"] = self.count
            return icon_data

        components: Dict[str, Any] = {}
        icon_id: str

        if isinstance(self.icon, Item):
            icon_id = f"{MINECRAFT_NAMESPACE}:{self.icon.base_item}"
            components = {
                f"{MINECRAFT_NAMESPACE}:{COMPONENT_CUSTOM_MODEL_DATA}": {
                    "strings": [f"{TASTY_SUPPLIES_NAMESPACE}/{self.icon.name}"]
                }
            }
        else:
            icon_id = ensure_namespace(str(self.icon), MINECRAFT_NAMESPACE)

        if self.components:
            components.update(deepcopy(self.components))

        icon_data: Dict[str, Any] = {"id": icon_id}

        if self.count != 1 or isinstance(self.icon, Item):
            icon_data["count"] = self.count

        if components:
            icon_data["components"] = components

        return icon_data

    def __repr__(self) -> str:
        return f"AdvancementIcon(icon={self.icon!r}, count={self.count})"


@dataclass(slots=True)
class AdvancementCriteria:
    """Single advancement criteria definition.

    Attributes:
        trigger: Advancement trigger identifier (e.g. ``"minecraft:impossible"``).
        conditions: Optional condition payload evaluated when the trigger fires.
        player: Optional player predicate(s); either a single predicate object or a
            list of predicates that must all pass. Not valid for the
            ``minecraft:impossible`` trigger.
        extra: Additional trigger-specific properties merged verbatim into the
            criteria payload (for advanced triggers like ``minecraft:tick``).
    """

    trigger: str
    conditions: Optional[Dict[str, Any]] = None
    player: Optional[PlayerPredicateType] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"trigger": self.trigger}

        if self.conditions:
            payload["conditions"] = deepcopy(self.conditions)

        if self.player is not None:
            payload["player"] = deepcopy(self.player)

        if self.extra:
            payload.update(deepcopy(self.extra))

        return payload

class AdvancementRewards:
    """Reward payload assigned upon advancement completion."""

    def __init__(
        self,
        experience: int = 0,
        recipes: Optional[List[Union[Recipe, str]]] = None,
        loot: Optional[List[str]] = None,
        function: Optional[str] = None,
    ) -> None:
        self.experience = experience
        self.recipes = list(recipes) if recipes else []
        self.loot = list(loot) if loot else []
        self.function = function

    def to_json(self) -> Dict[str, Any]:
        rewards: Dict[str, Any] = {}
        if self.experience:
            rewards["experience"] = self.experience
        if self.recipes:
            rewards["recipes"] = [r.recipe_id if isinstance(r, Recipe) else r for r in self.recipes]
        if self.loot:
            rewards["loot"] = list(self.loot)
        if self.function:
            rewards["function"] = self.function
        return rewards

    def __repr__(self) -> str:
        return (
            "AdvancementRewards("
            f"experience={self.experience}, recipes={self.recipes}, "
            f"loot={self.loot}, function={self.function})"
        )


class Advancement:
    """Represent a single advancement entry that can be registered with Beet."""

    def __init__(
        self,
        advancement_id: str,
        title: str,
        icon: Union[AdvancementIcon, IconType],
        criteria: CriteriaMapping,
        *,
        parent: Optional[Union["Advancement", str]] = None,
        description: str = "",
        advancement_type: ADVANCEMENT_TYPE = ADVANCEMENT_TYPE.TASK,
        requirements: Optional[List[List[str]]] = None,
        rewards: Optional[AdvancementRewards] = None,
        background: Optional[str] = None,
        show_toast: bool = True,
        announce_to_chat: bool = False,
        hidden: bool = False,
        sends_telemetry_event: bool = True,
        display_extras: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.advancement_id = advancement_id
        self.parent = parent
        self.title = title
        self.description = description
        self.icon = icon if isinstance(icon, AdvancementIcon) else AdvancementIcon(icon)
        self.criteria: CriteriaMapping = {
            name: criteria if isinstance(criteria, AdvancementCriteria) else deepcopy(criteria)
            for name, criteria in criteria.items()
        }
        self.requirements = requirements or [list(criteria.keys())]
        self.rewards = rewards
        self.type = advancement_type
        self.background = background
        self.show_toast = show_toast
        self.announce_to_chat = announce_to_chat
        self.hidden = hidden
        self.sends_telemetry_event = sends_telemetry_event
        self.display_extras = display_extras or {}

    @property
    def qualified_id(self) -> str:
        return ensure_namespace(
            self.advancement_id,
            TASTY_SUPPLIES_NAMESPACE,
            allow_tags=False,
        )

    def _resolve_parent(self) -> Optional[str]:
        if self.parent is None:
            return None
        if isinstance(self.parent, Advancement):
            return self.parent.qualified_id
        return ensure_namespace(
            self.parent,
            TASTY_SUPPLIES_NAMESPACE,
            allow_tags=False,
        )

    def _to_json(self) -> Dict[str, Any]:
        display: Dict[str, Any] = {
            "title": self.title,
            "description": self.description,
            "icon": self.icon.to_json(),
            "frame": self.type.value,
            "show_toast": self.show_toast,
            "announce_to_chat": self.announce_to_chat,
        }

        if self.background:
            display["background"] = self.background
        if self.hidden:
            display["hidden"] = True

        if self.display_extras:
            display.update(deepcopy(self.display_extras))

        criteria_payload: Dict[str, Any] = {}
        for name, criteria in self.criteria.items():
            if isinstance(criteria, AdvancementCriteria):
                criteria_payload[name] = criteria.to_json()
            else:
                criteria_payload[name] = deepcopy(criteria)

        data: Dict[str, Any] = {
            "display": display,
            "criteria": criteria_payload,
            "requirements": deepcopy(self.requirements),
            "sends_telemetry_event": self.sends_telemetry_event,
        }

        parent_id = self._resolve_parent()
        if parent_id:
            data["parent"] = parent_id

        if self.rewards:
            rewards_payload = self.rewards.to_json()
            if rewards_payload:
                data["rewards"] = rewards_payload

        return data

    def register(self, ctx: TSContext) -> None:
        """Register this advancement with the Beet context."""

        advancement_json = self._to_json()
        ctx.data[TASTY_SUPPLIES_NAMESPACE].advancements[self.advancement_id] = BeetAdvancement(
            advancement_json
        )
        log.debug(f"Registered advancement '{self.advancement_id}'")

    def __repr__(self) -> str:
        return f"Advancement(id='{self.advancement_id}', title='{self.title}')"