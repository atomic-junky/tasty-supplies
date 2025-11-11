"""Data-driven crop system for Tasty Supplies.

This module defines the configuration structures and runtime generator that
produce all datapack resources related to custom crops. Crops are described
through simple dataclasses so new entries can be added without touching the
generation logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence

from beet import Function, LootTable, Model

from ..bucket import Bucket
from ..logger import log
from ..models.context import TSContext
from ..utils import to_snbt


@dataclass
class DropConfig:
    """Configuration for a harvest drop entry."""

    item: str
    min_count: int = 1
    max_count: int = 1
    chance: float = 1.0


@dataclass
class CropDefinition:
    """Fully describes a crop and its related resources."""

    name: str
    seed_base_item: str
    seed_texture: str
    produce_base_item: str
    produce_texture: str
    stage_textures: Sequence[str]
    growth_interval: int
    conversion_block: str = "minecraft:wheat[age=0]"
    soil_block: str = "minecraft:farmland"
    produce_item_name: str = ""
    create_produce_item: bool = True
    produce_components: Optional[Dict[str, dict]] = None
    harvest_drops: Sequence[DropConfig] = field(default_factory=list)

    stage_model_ids: List[str] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not self.produce_item_name:
            self.produce_item_name = self.name

    @property
    def seed_item_name(self) -> str:
        return f"{self.name}_seeds"

    def validate(self) -> None:
        if not self.stage_textures:
            raise ValueError(f"Crop '{self.name}' requires at least one stage texture.")
        if self.growth_interval <= 0:
            raise ValueError(
                f"Crop '{self.name}' must have a positive growth interval."
            )


@dataclass
class UsageObjective:
    """Tracks scoreboard objective names for seed usage."""

    base_item: str
    usage_objective: str
    last_objective: str


class CropManager:
    """Generate datapack resources for registered crops."""

    def __init__(
        self,
        ctx: TSContext,
        bucket: Bucket,
        definitions: Iterable[CropDefinition],
    ) -> None:
        self.ctx = ctx
        self.bucket = bucket
        self.definitions: List[CropDefinition] = list(definitions)
        for definition in self.definitions:
            definition.validate()

        base_items = sorted(
            {definition.seed_base_item for definition in self.definitions}
        )
        self.usage_objectives: List[UsageObjective] = [
            UsageObjective(
                base_item=base_item,
                usage_objective=f"tsc_u{i}",
                last_objective=f"tsc_l{i}",
            )
            for i, base_item in enumerate(base_items)
        ]

    def register(self) -> None:
        """Create all assets and functions for the configured crops."""

        if not self.definitions:
            return

        self._create_stage_models()
        self._create_loot_tables()
        self._create_load_function()
        self._create_tick_functions()
        self._create_seed_functions()
        self._create_crop_functions()

    # ------------------------------------------------------------------
    # Asset generation
    # ------------------------------------------------------------------

    def _create_stage_models(self) -> None:
        assets = self.ctx.assets["tasty_supplies"].models
        for definition in self.definitions:
            definition.stage_model_ids.clear()
            for index, texture in enumerate(definition.stage_textures):
                # Place crop stage models under models/block and reference them as tasty_supplies:block/*
                model_name = f"block/{definition.name}_stage{index}"
                model_id = f"tasty_supplies:block/{definition.name}_stage{index}"
                # Use texture key 'cross' to override parent minecraft:block/cross properly.
                model = {
                    "parent": "tasty_supplies:block/crop_cross",
                    "textures": {"cross": texture, "particle": texture},
                }
                assets[model_name] = Model(model)
                definition.stage_model_ids.append(model_id)

    def _create_loot_tables(self) -> None:
        # Use string path indexing to forcefully create files under loot_tables/ (not loot_table/)
        for definition in self.definitions:
            if not definition.harvest_drops:
                continue

            pools: List[Dict[str, object]] = []
            entries: List[Dict[str, object]] = []

            for drop in definition.harvest_drops:
                entry = self._build_loot_entry(drop)
                if entry:
                    entries.append(entry)

            if entries:
                pools.append({"rolls": 1, "entries": entries})

            if pools:
                # Directly use __setitem__ on the DataPack container with full path
                self.ctx.data[f"tasty_supplies"][f"crops/{definition.name}"] = (
                    LootTable({"pools": pools})
                )

    def _build_loot_entry(self, drop: DropConfig) -> Optional[Dict[str, object]]:
        if drop.min_count > drop.max_count:
            log.warning(
                "Skipping drop for %s: min_count greater than max_count.", drop.item
            )
            return None

        entry: Dict[str, object] = {"type": "minecraft:item"}

        if self.bucket.contains_item(drop.item):
            item = self.bucket.get(drop.item)
            if item is None:
                return None
            result = item.to_result()
            entry["name"] = result["id"]
            components = result.get("components")
            if components:
                entry.setdefault("functions", []).append(
                    {"function": "minecraft:set_components", "components": components}
                )
        else:
            entry["name"] = drop.item

        if drop.min_count == drop.max_count:
            if drop.min_count != 1:
                entry.setdefault("functions", []).append(
                    {"function": "minecraft:set_count", "count": drop.min_count}
                )
        else:
            entry.setdefault("functions", []).append(
                {
                    "function": "minecraft:set_count",
                    "count": {
                        "type": "minecraft:uniform",
                        "min": drop.min_count,
                        "max": drop.max_count,
                    },
                }
            )

        if drop.chance < 1.0:
            entry.setdefault("conditions", []).append(
                {"condition": "minecraft:random_chance", "chance": drop.chance}
            )

        return entry

    # ------------------------------------------------------------------
    # Function generation
    # ------------------------------------------------------------------

    def _create_load_function(self) -> None:
        commands = [
            "scoreboard objectives add tsc_age dummy",
            "scoreboard objectives add tsc_max dummy",
            "scoreboard objectives add tsc_timer dummy",
            "scoreboard objectives add tsc_int dummy",
            "scoreboard objectives add tsc_tmp dummy",
        ]

        for objective in self.usage_objectives:
            commands.append(
                f"scoreboard objectives add {objective.usage_objective} "
                f"minecraft.used:minecraft.{objective.base_item}"
            )
            commands.append(
                f"scoreboard objectives add {objective.last_objective} dummy"
            )

        self.ctx.data["tasty_supplies"].functions["load"] = Function(commands)

    def _create_tick_functions(self) -> None:
        tick_lines: List[str] = []

        for objective in self.usage_objectives:
            base = objective.base_item
            tick_lines.append(
                f"execute as @a if score @s {objective.usage_objective} > @s {objective.last_objective} "
                f"run function tasty_supplies:seeds/base/{base}"
            )
            tick_lines.append(
                f"execute as @a if score @s {objective.usage_objective} > @s {objective.last_objective} "
                f"run scoreboard players operation @s {objective.last_objective} = @s {objective.usage_objective}"
            )

        tick_lines.append("function tasty_supplies:crops/internal/grow")

        # Integrate hit & interact detection each tick (per player)
        tick_lines.append("execute as @a run function tasty_supplies:hit_crop/main")
        tick_lines.append(
            "execute as @a run function tasty_supplies:interact_crop/main"
        )
        self.ctx.data["tasty_supplies"].functions["crops/tick"] = Function(tick_lines)

        grow_lines = [
            "execute as @e[type=minecraft:item_display,tag=ts.crop] at @s run function "
            "tasty_supplies:crops/internal/grow_single"
        ]
        self.ctx.data["tasty_supplies"].functions["crops/internal/grow"] = Function(
            grow_lines
        )

        grow_single_lines = [
            "execute unless block ~ ~-1 ~ minecraft:farmland run function "
            "tasty_supplies:crops/internal/despawn",
            "execute if entity @s run scoreboard players add @s tsc_timer 1",
            "execute if entity @s if score @s tsc_timer >= @s tsc_int run function "
            "tasty_supplies:crops/internal/advance",
            # Maintain alignment & interaction entity mount per tick
            "function tasty_supplies:crops/internal/sync",
        ]
        self.ctx.data["tasty_supplies"].functions["crops/internal/grow_single"] = (
            Function(grow_single_lines)
        )

        despawn_lines = [
            "say [DEBUG] Crop despawned (farmland removed)",
            "execute if score @s tsc_age >= @s tsc_max run function "
            "tasty_supplies:crops/internal/drop_ready",
            "kill @s",
        ]
        self.ctx.data["tasty_supplies"].functions["crops/internal/despawn"] = Function(
            despawn_lines
        )

        advance_lines = [
            "scoreboard players add @s tsc_age 1",
            "execute if score @s tsc_age > @s tsc_max run scoreboard players operation @s tsc_age = @s tsc_max",
            "scoreboard players operation @s tsc_timer -= @s tsc_int",
            "execute if score @s tsc_timer matches ..-1 run scoreboard players set @s tsc_timer 0",
        ]
        for definition in self.definitions:
            advance_lines.append(
                f"execute if entity @s[tag=ts.crop.{definition.name}] run function "
                f"tasty_supplies:crops/{definition.name}/update"
            )
        self.ctx.data["tasty_supplies"].functions["crops/internal/advance"] = Function(
            advance_lines
        )

        drop_ready_lines: List[str] = []
        for definition in self.definitions:
            drop_ready_lines.append(
                f"execute if entity @s[tag=ts.crop.{definition.name}] run function "
                f"tasty_supplies:crops/{definition.name}/harvest"
            )
        drop_ready_lines.append("kill @s")
        self.ctx.data["tasty_supplies"].functions["crops/internal/drop_ready"] = (
            Function(drop_ready_lines)
        )

        # Keep crop entity centered and interaction entity mounted for hit/interact simulation
        sync_lines = [
            "execute align xyz run tp @s ~0.5 ~ ~0.5",
            "data modify entity @s transformation.translation set value [0f,0f,0f]",
            # Summon interaction entity if missing
            'execute unless entity @e[type=minecraft:interaction,tag=ts.crop_interaction,limit=1,distance=..0.2] run summon minecraft:interaction ~ ~-0.5625 ~ {Tags:["ts.crop_interaction"]}',
            # Mount interaction entity onto crop display
            "execute positioned ~ ~-0.5625 ~ run ride @e[type=minecraft:interaction,tag=ts.crop_interaction,sort=nearest,limit=1,distance=..1] mount @s",
        ]
        self.ctx.data["tasty_supplies"].functions["crops/internal/sync"] = Function(
            sync_lines
        )

        # Player punch detection
        hit_main_lines = [
            "scoreboard players set $ts_hit_check tsc_tmp 0",
            "tag @s add ts.hit_crop",
            "execute as @e[type=minecraft:interaction,tag=ts.crop_interaction,distance=..20] at @s run function tasty_supplies:hit_crop/check",
            "tag @s remove ts.hit_crop",
        ]
        self.ctx.data["tasty_supplies"].functions["hit_crop/main"] = Function(
            hit_main_lines
        )

        hit_check_lines = [
            "execute if score $ts_hit_check tsc_tmp matches 1 run return run data remove entity @s attack",
            "execute on attacker if entity @s[tag=ts.hit_crop] run scoreboard players set $ts_hit_check tsc_tmp 1",
            "data remove entity @s attack",
            "execute if score $ts_hit_check tsc_tmp matches 1 on vehicle if entity @s[type=minecraft:item_display,tag=ts.crop] at @s run function tasty_supplies:hit_crop/switch",
        ]
        self.ctx.data["tasty_supplies"].functions["hit_crop/check"] = Function(
            hit_check_lines
        )

        hit_switch_lines: List[str] = []
        for definition in self.definitions:
            hit_switch_lines.append(
                f"execute if entity @s[tag=ts.crop.{definition.name}] run return run function tasty_supplies:crops/{definition.name}/harvest"
            )
        self.ctx.data["tasty_supplies"].functions["hit_crop/switch"] = Function(
            hit_switch_lines
        )

        # Player interact detection (for bonemeal/tools)
        interact_main_lines = [
            "scoreboard players set $ts_interact_check tsc_tmp 0",
            "tag @s add ts.interact_crop",
            "execute as @e[type=minecraft:interaction,tag=ts.crop_interaction,distance=..20] at @s run function tasty_supplies:interact_crop/check",
            "tag @s remove ts.interact_crop",
        ]
        self.ctx.data["tasty_supplies"].functions["interact_crop/main"] = Function(
            interact_main_lines
        )

        interact_check_lines = [
            "execute if score $ts_interact_check tsc_tmp matches 1 run return run data remove entity @s interaction",
            "execute on target if entity @s[tag=ts.interact_crop] run scoreboard players set $ts_interact_check tsc_tmp 1",
            "data remove entity @s interaction",
            "execute if score $ts_interact_check tsc_tmp matches 0 run return fail",
            "execute on vehicle if entity @s[type=minecraft:item_display,tag=ts.crop] run function tasty_supplies:interact_crop/switch",
        ]
        self.ctx.data["tasty_supplies"].functions["interact_crop/check"] = Function(
            interact_check_lines
        )

        interact_switch_lines = [
            "execute as @p[tag=ts.interact_crop,sort=nearest,limit=1,distance=..3] if items entity @s weapon.mainhand minecraft:bone_meal run function tasty_supplies:crops/internal/bonemeal",
        ]
        self.ctx.data["tasty_supplies"].functions["interact_crop/switch"] = Function(
            interact_switch_lines
        )

        bonemeal_lines: List[str] = [
            "clear @s minecraft:bone_meal 1",
            "scoreboard players add @e[type=minecraft:item_display,tag=ts.crop,limit=1,sort=nearest,distance=..0.1] tsc_age 1",
            "execute as @e[type=minecraft:item_display,tag=ts.crop,limit=1,sort=nearest,distance=..0.1] if score @s tsc_age > @s tsc_max run scoreboard players operation @s tsc_age = @s tsc_max",
            "scoreboard players set @e[type=minecraft:item_display,tag=ts.crop,limit=1,sort=nearest,distance=..0.1] tsc_timer 0",
        ]
        for definition in self.definitions:
            bonemeal_lines.append(
                f"execute as @e[type=minecraft:item_display,tag=ts.crop.{definition.name},limit=1,sort=nearest,distance=..0.1] run function tasty_supplies:crops/{definition.name}/update"
            )
        self.ctx.data["tasty_supplies"].functions["crops/internal/bonemeal"] = Function(
            bonemeal_lines
        )

    def _create_seed_functions(self) -> None:
        seeds_namespace = self.ctx.data["tasty_supplies"].functions
        for objective in self.usage_objectives:
            lines: List[str] = []
            for definition in self.definitions:
                if definition.seed_base_item != objective.base_item:
                    continue
                base_item_id = definition.seed_base_item
                if ":" not in base_item_id:
                    base_item_id = f"minecraft:{base_item_id}"

                component_snbt = to_snbt(
                    {"strings": [f"tasty_supplies/{definition.seed_item_name}"]}
                )

                lines.append(
                    "execute if items entity @s weapon.mainhand "
                    + base_item_id
                    + f"[minecraft:custom_model_data={component_snbt}] run function "
                    f"tasty_supplies:crops/{definition.name}/plant"
                )
                lines.append(
                    "execute if items entity @s weapon.offhand "
                    + base_item_id
                    + f"[minecraft:custom_model_data={component_snbt}] run function "
                    f"tasty_supplies:crops/{definition.name}/plant"
                )
            seeds_namespace[f"seeds/base/{objective.base_item}"] = Function(lines)

    def _create_crop_functions(self) -> None:
        functions = self.ctx.data["tasty_supplies"].functions

        offsets = [
            (0, 0, 0),
            (1, 0, 0),
            (-1, 0, 0),
            (0, 0, 1),
            (0, 0, -1),
            (1, 0, 1),
            (1, 0, -1),
            (-1, 0, 1),
            (-1, 0, -1),
            (0, 1, 0),
            (0, 1, 1),
            (0, 1, -1),
            (1, 1, 0),
            (-1, 1, 0),
        ]

        for definition in self.definitions:
            plant_lines: List[str] = []
            for dx, dy, dz in offsets:
                position = self._offset_to_command(dx, dy, dz)
                plant_lines.append(
                    "execute positioned "
                    f"{position} if block ~ ~ ~ {definition.conversion_block} "
                    f"if block ~ ~-1 ~ {definition.soil_block} run function "
                    f"tasty_supplies:crops/{definition.name}/internal/spawn"
                )
            functions[f"crops/{definition.name}/plant"] = Function(plant_lines)

            spawn_lines = [
                "setblock ~ ~ ~ air",
                "playsound minecraft:item.crop.plant block @a ~ ~ ~ 1 1",
                f"say [DEBUG] Planted {definition.name} crop",
                self._summon_crop_command(definition),
                f"scoreboard players set @e[type=minecraft:item_display,tag=ts.crop.new,limit=1,distance=..0.1] tsc_age 0",
                f"scoreboard players set @e[type=minecraft:item_display,tag=ts.crop.new,limit=1,distance=..0.1] tsc_max {len(definition.stage_model_ids) - 1}",
                f"scoreboard players set @e[type=minecraft:item_display,tag=ts.crop.new,limit=1,distance=..0.1] tsc_timer 0",
                f"scoreboard players set @e[type=minecraft:item_display,tag=ts.crop.new,limit=1,distance=..0.1] tsc_int {definition.growth_interval}",
                "tag @e[type=minecraft:item_display,tag=ts.crop.new,limit=1,distance=..0.1] remove ts.crop.new",
            ]
            functions[f"crops/{definition.name}/internal/spawn"] = Function(spawn_lines)

            update_lines: List[str] = []
            for index, model_id in enumerate(definition.stage_model_ids):
                update_lines.append(
                    f'execute if score @s tsc_age matches {index} run data modify entity @s item.components."minecraft:item_model" set value "{model_id}"'
                )
            # Add debug message for growth stage updates
            update_lines.append(
                f"execute store result score #debug_age tsc_int run scoreboard players get @s tsc_age"
            )
            update_lines.append(f"say [DEBUG] {definition.name} grew to stage")
            # Do not auto-harvest on final stage; allow farmland break (despawn) to trigger harvest.
            functions[f"crops/{definition.name}/update"] = Function(update_lines)

            harvest_lines: List[str] = []
            harvest_lines.append(f"say [DEBUG] Harvesting {definition.name}")
            if definition.harvest_drops:
                # Reference actual Beet loot_table/ path (singular) to match what we write
                harvest_lines.append(
                    f"loot spawn ~ ~ ~ loot tasty_supplies:crops/{definition.name}"
                )
                harvest_lines.append(f"say [DEBUG] Loot spawned for {definition.name}")
            harvest_lines.append("kill @s")
            functions[f"crops/{definition.name}/harvest"] = Function(harvest_lines)

    # ------------------------------------------------------------------
    # Helper utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _offset_to_command(dx: int, dy: int, dz: int) -> str:
        return f"~{dx if dx else ''} ~{dy if dy else ''} ~{dz if dz else ''}"

    @staticmethod
    def _summon_crop_command(definition: CropDefinition) -> str:
        model = definition.stage_model_ids[0]
        return (
            'summon minecraft:item_display ~0.5 ~ ~0.5 {item_display:"ground",'
            f'Tags:["ts.crop","ts.crop.{definition.name}","ts.crop.new"],'
            f'item:{{id:"minecraft:barrier",count:1,components:{{"minecraft:item_model":"{model}",'
            f'custom_data:{{tasty_supplies:{{seed:"{definition.name}"}}}}}}}},'
            "transformation:{left_rotation:{angle:0f,axis:[0f,1f,0f]},right_rotation:{angle:0f,axis:[0f,1f,0f]},"
            "translation:[0f,0f,0f],scale:[1f,1f,1f]}}"
        )
