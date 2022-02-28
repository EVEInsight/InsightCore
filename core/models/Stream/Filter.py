from dataclasses import dataclass, asdict, field
from core.models.BaseModel import BaseModel


@dataclass
class Filter(BaseModel):
    _km_min_fittedValue: float = 0.0
    _km_max_fittedValue: float = float("inf")
    _km_min_droppedValue: float = 0.0
    _km_max_droppedValue: float = float("inf")
    _km_min_destroyedValue: float = 0.0
    _km_max_destroyedValue: float = float("inf")
    _km_min_totalValue: float = 0.0
    _km_max_totalValue: float = float("inf")
    _km_min_points: float = 0.0
    _km_max_points: float = float("inf")
    _km_require_npc: bool = False
    _km_require_solo: bool = False
    _km_require_awox: bool = False
    _km_min_age_seconds: int = 0
    _km_max_age_seconds: int = float("inf")

    _attackers_min: int = 0
    _attackers_max: int = float("inf")
    _attacker_min_security_status: float = float("-inf")
    _attacker_max_security_status: float = float("inf")
    _attacker_min_damage_done: float = 0.0
    _attacker_max_damage_done: float = float("inf")
    _attacker_alliance_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_alliance_ids_exclude: list[int] = field(default_factory=list)
    _attacker_character_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_character_ids_exclude: list[int] = field(default_factory=list)
    _attacker_corporation_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_corporation_ids_exclude: list[int] = field(default_factory=list)
    _attacker_faction_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_faction_ids_exclude: list[int] = field(default_factory=list)

    _attacker_ship_category_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_ship_category_ids_exclude: list[int] = field(default_factory=list)
    _attacker_ship_group_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_ship_group_ids_exclude: list[int] = field(default_factory=list)
    _attacker_ship_type_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_ship_type_ids_exclude: list[int] = field(default_factory=list)

    _attacker_weapon_category_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_weapon_category_ids_exclude: list[int] = field(default_factory=list)
    _attacker_weapon_group_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_weapon_group_ids_exclude: list[int] = field(default_factory=list)
    _attacker_weapon_type_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _attacker_weapon_type_ids_exclude: list[int] = field(default_factory=list)

    _victim_min_damaged_taken: float = 0.0
    _victim_max_damaged_taken: float = float("inf")
    _victim_alliance_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _victim_alliance_ids_exclude: list[int] = field(default_factory=list)
    _victim_character_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _victim_character_ids_exclude: list[int] = field(default_factory=list)
    _victim_corporation_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _victim_corporation_ids_exclude: list[int] = field(default_factory=list)
    _victim_faction_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _victim_faction_ids_exclude: list[int] = field(default_factory=list)

    _victim_ship_category_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _victim_ship_category_ids_exclude: list[int] = field(default_factory=list)
    _victim_ship_group_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _victim_ship_group_ids_exclude: list[int] = field(default_factory=list)
    _victim_ship_type_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _victim_ship_type_ids_exclude: list[int] = field(default_factory=list)

    _region_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _region_ids_exclude: list[int] = field(default_factory=list)
    _constellation_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _constellation_ids_exclude: list[int] = field(default_factory=list)
    _system_min_security_status: float = float("-inf")
    _system_max_security_status: float = float("inf")
    _system_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _system_ranges_gate_include: list[int] = field(default_factory=list)
    _system_ranges_lightyear_include: list[int] = field(default_factory=list)
    _system_ids_exclude: list[int] = field(default_factory=list)

    _location_ids_include: list[int] = field(default_factory=lambda: ["*"])
    _location_ids_exclude: list[int] = field(default_factory=list)

