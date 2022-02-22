from dataclasses import dataclass


@dataclass
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
    alliance_name: str = ""
    character_name: str = ""
    corporation_name: str = ""
    faction_name: str = ""

    # unresolved ship info requiring api call
    ship_type_name: str = ""
    ship_group_id: int = None
    ship_group_name: str = ""
    ship_category_id: int = None
    ship_category_name: str = ""

    # unresolved ship weapon type info requiring api call
    weapon_type_name: str = ""
    weapon_group_id: int = None
    weapon_group_name: str = ""
    weapon_category_id: int = None
    weapon_category_name: str = ""

    @classmethod
    def json_decode_from_zk(cls, dct):
        return cls(damage_done=dct["damage_done"],
                   final_blow=dct["final_blow"],
                   security_status=dct["security_status"],
                   alliance_id=dct.get("alliance_id"),
                   character_id=dct.get("character_id"),
                   corporation_id=dct.get("corporation_id"),
                   faction_id=dct.get("faction_id"),
                   ship_type_id=dct.get("ship_type_id"),
                   weapon_type_id=dct.get("weapon_type_id")
                   )

    @classmethod
    def json_decode_multi_from_zk(cls, dct):
        a = []
        attackers_json = list(dct["package"]["killmail"]["attackers"])
        for attacker_json in attackers_json:
            a.append(cls.json_decode_from_zk(attacker_json))
        return a
