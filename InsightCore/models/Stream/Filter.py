from dataclasses import dataclass, field
from InsightCore.models.BaseModel import BaseModel


@dataclass
class Filter(BaseModel):
    km_min_fittedValue: float = 0.0
    km_max_fittedValue: float = float("inf")
    km_min_droppedValue: float = 0.0
    km_max_droppedValue: float = float("inf")
    km_min_destroyedValue: float = 0.0
    km_max_destroyedValue: float = float("inf")
    km_min_totalValue: float = 0.0
    km_max_totalValue: float = float("inf")
    km_min_points: float = 0.0
    km_max_points: float = float("inf")
    km_require_npc: bool = False
    km_require_solo: bool = False
    km_require_awox: bool = False
    km_min_age_seconds: int = 0
    km_max_age_seconds: int = float("inf")

    attackers_min: int = 0
    attackers_max: int = float("inf")
    attacker_min_security_status: float = float("-inf")
    attacker_max_security_status: float = float("inf")
    attacker_min_damage_done: float = 0.0
    attacker_max_damage_done: float = float("inf")
    attacker_alliance_ids_include: list[int] = field(default_factory=list)
    attacker_alliance_ids_exclude: list[int] = field(default_factory=list)
    attacker_character_ids_include: list[int] = field(default_factory=list)
    attacker_character_ids_exclude: list[int] = field(default_factory=list)
    attacker_corporation_ids_include: list[int] = field(default_factory=list)
    attacker_corporation_ids_exclude: list[int] = field(default_factory=list)
    attacker_faction_ids_include: list[int] = field(default_factory=lambda: ["*"])
    attacker_faction_ids_exclude: list[int] = field(default_factory=list)

    attacker_ship_category_ids_include: list[int] = field(default_factory=lambda: ["*"])
    attacker_ship_category_ids_exclude: list[int] = field(default_factory=list)
    attacker_ship_group_ids_include: list[int] = field(default_factory=lambda: ["*"])
    attacker_ship_group_references_include: list[str] = field(default_factory=list)
    attacker_ship_group_ids_exclude: list[int] = field(default_factory=list)
    attacker_ship_group_references_exclude: list[str] = field(default_factory=list)
    attacker_ship_type_ids_include: list[int] = field(default_factory=lambda: ["*"])
    attacker_ship_type_references_include: list[str] = field(default_factory=list)
    attacker_ship_type_ids_exclude: list[int] = field(default_factory=list)
    attacker_ship_type_references_exclude: list[str] = field(default_factory=list)
    attacker_min_ship_adjusted_price: float = float("-inf")
    attacker_max_ship_adjusted_price: float = float("inf")

    attacker_weapon_category_ids_include: list[int] = field(default_factory=lambda: ["*"])
    attacker_weapon_category_ids_exclude: list[int] = field(default_factory=list)
    attacker_weapon_group_ids_include: list[int] = field(default_factory=lambda: ["*"])
    attacker_weapon_group_ids_exclude: list[int] = field(default_factory=list)
    attacker_weapon_type_ids_include: list[int] = field(default_factory=lambda: ["*"])
    attacker_weapon_type_ids_exclude: list[int] = field(default_factory=list)

    victim_min_damage_taken: float = 0.0
    victim_max_damage_taken: float = float("inf")
    victim_alliance_ids_include: list[int] = field(default_factory=list)
    victim_alliance_ids_exclude: list[int] = field(default_factory=list)
    victim_character_ids_include: list[int] = field(default_factory=list)
    victim_character_ids_exclude: list[int] = field(default_factory=list)
    victim_corporation_ids_include: list[int] = field(default_factory=list)
    victim_corporation_ids_exclude: list[int] = field(default_factory=list)
    victim_faction_ids_include: list[int] = field(default_factory=lambda: ["*"])
    victim_faction_ids_exclude: list[int] = field(default_factory=list)

    victim_ship_category_ids_include: list[int] = field(default_factory=lambda: ["*"])
    victim_ship_category_ids_exclude: list[int] = field(default_factory=list)
    victim_ship_group_ids_include: list[int] = field(default_factory=lambda: ["*"])
    victim_ship_group_references_include: list[str] = field(default_factory=list)
    victim_ship_group_ids_exclude: list[int] = field(default_factory=list)
    victim_ship_group_references_exclude: list[str] = field(default_factory=list)
    victim_ship_type_ids_include: list[int] = field(default_factory=lambda: ["*"])
    victim_ship_type_references_include: list[str] = field(default_factory=list)
    victim_ship_type_ids_exclude: list[int] = field(default_factory=list)
    victim_ship_type_references_exclude: list[str] = field(default_factory=list)

    region_ids_include: list[int] = field(default_factory=lambda: ["*"])
    region_ids_exclude: list[int] = field(default_factory=list)
    constellation_ids_include: list[int] = field(default_factory=lambda: ["*"])
    constellation_ids_exclude: list[int] = field(default_factory=list)
    system_min_security_status: float = float("-inf")
    system_max_security_status: float = float("inf")
    system_ids_include: list[int] = field(default_factory=lambda: ["*"])
    system_ranges_gate_include: list[int] = field(default_factory=list)
    system_ranges_lightyear_include: list[int] = field(default_factory=list)
    system_ids_exclude: list[int] = field(default_factory=list)

    location_ids_include: list[int] = field(default_factory=lambda: ["*"])
    location_ids_exclude: list[int] = field(default_factory=list)

