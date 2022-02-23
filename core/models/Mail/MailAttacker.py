from dataclasses import dataclass


@dataclass(init=False)
class MailAttacker:
    """
    mail attacker representing data for Insight parsed from ZK json and additional attributes resolved through ESI
    """
    # directly resolved through zk mail json - required

    damage_done: int
    final_blow: bool
    security_status: float

    # directly resolved through zk mail json - optional
    alliance_id: int = None
    character_id: int = None
    corporation_id: int = None
    faction_id: int = None
    ship_type_id: int = None
    weapon_type_id: int = None

    # unresolved entity names requiring api call
    alliance_name: str = None
    character_name: str = None
    corporation_name: str = None
    faction_name: str = None

    # unresolved ship info requiring api call
    ship_type_name: str = None
    ship_group_id: int = None
    ship_group_name: str = None
    ship_category_id: int = None
    ship_category_name: str = None

    # unresolved ship weapon type info requiring api call
    weapon_type_name: str = None
    weapon_group_id: int = None
    weapon_group_name: str = None
    weapon_category_id: int = None
    weapon_category_name: str = None

    def __init__(self, dct: dict):
        for k, v in dct.items():
            setattr(self, k, v)

    @classmethod
    def from_json(cls, dct):
        return cls(dct)


@dataclass(init=False)
class RedisQMailAttacker(MailAttacker):
    def __init__(self, dct: dict):
        setattr(self, "damage_done",        dct["damage_done"])
        setattr(self, "final_blow",         dct["final_blow"])
        setattr(self, "security_status",    dct["security_status"])
        setattr(self, "alliance_id",        dct.get("alliance_id"))
        setattr(self, "character_id",       dct.get("character_id"))
        setattr(self, "corporation_id",     dct.get("corporation_id"))
        setattr(self, "faction_id",         dct.get("faction_id"))
        setattr(self, "ship_type_id",       dct.get("ship_type_id"))
        setattr(self, "weapon_type_id",     dct.get("weapon_type_id"))

    @classmethod
    def from_json(cls, dct):
        return cls(dct)
