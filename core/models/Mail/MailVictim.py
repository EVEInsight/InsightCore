from dataclasses import dataclass


@dataclass(init=False)
class MailVictim:
    """
    mail victim representing data for Insight parsed from ZK json and additional attributes resolved through ESI
    """
    # directly resolved through zk mail json - required
    damaged_taken: int
    ship_type_id: int

    # directly resolved through zk mail json - optional
    alliance_id: int = None
    character_id: int = None
    corporation_id: int = None
    faction_id: int = None
    # items: list[MailItem] = field(default_factory=list) # todo add items
    position_x: float = None
    position_y: float = None
    position_z: float = None

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

    def __init__(self, dct: dict):
        for k, v in dct.items():
            setattr(self, k, v)

    @classmethod
    def from_json(cls, dct):
        return cls(dct)


@dataclass(init=False)
class RedisQVictim(MailVictim):
    def __init__(self, dct: dict):
        setattr(self, "damaged_taken",  dct["damage_taken"])
        setattr(self, "ship_type_id",   dct.get("ship_type_id"))
        setattr(self, "alliance_id",    dct.get("alliance_id"))
        setattr(self, "character_id",   dct.get("character_id"))
        setattr(self, "corporation_id", dct.get("corporation_id"))
        setattr(self, "faction_id",     dct.get("faction_id"))
        setattr(self, "position_x",     dct.get("position", {}).get("x"))
        setattr(self, "position_y",     dct.get("position", {}).get("y"))
        setattr(self, "position_z",     dct.get("position", {}).get("z"))

    @classmethod
    def from_json(cls, dct):
        return cls(dct)
