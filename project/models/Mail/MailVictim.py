from dataclasses import dataclass, field

@dataclass
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

    # unresolved ship info requiring api call
    ship_type_name: str = ""
    ship_group_id: int = None
    ship_group_name: str = ""
    ship_category_id: int = None
    ship_category_name: str = ""

    @classmethod
    def json_decode_from_zk(cls, dct):
        d = dct["package"]["killmail"]["victim"]
        return cls(damaged_taken=d["damage_taken"],
                   ship_type_id=d.get("ship_type_id"),
                   alliance_id=d.get("alliance_id"),
                   character_id=d.get("character_id"),
                   corporation_id=d.get("corporation_id"),
                   faction_id=d.get("faction_id"),
                   position_x=d.get("position", {}).get("x"),
                   position_y=d.get("position", {}).get("y"),
                   position_z=d.get("position", {}).get("z"),
                   )


