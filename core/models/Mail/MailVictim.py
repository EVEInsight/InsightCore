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
    _alliance_name: str = None
    _character_name: str = None
    _corporation_name: str = None
    _faction_name: str = None

    # unresolved ship info requiring api call
    _ship_type_name: str = None
    _ship_group_id: int = None
    _ship_group_name: str = None
    _ship_category_id: int = None
    _ship_category_name: str = None

    def __init__(self, dct: dict):
        for k, v in dct.items():
            setattr(self, k, v)

    @classmethod
    def from_json(cls, dct):
        """Returns an instance of class from a json dictionary

        :param dct: Dictionary returned from the to_json() method
        :return: An instance of the class
        :rtype: MailVictim
        """
        return cls(dct)

    @property
    def alliance_name(self):
        return self._alliance_name

    @alliance_name.setter
    def alliance_name(self, esi: dict):
        self._alliance_name = esi["name"]

    @property
    def character_name(self):
        return self._character_name

    @character_name.setter
    def character_name(self, esi: dict):
        self._character_name = esi["name"]

    @property
    def corporation_name(self):
        return self._corporation_name

    @corporation_name.setter
    def corporation_name(self, esi: dict):
        self._corporation_name = esi["name"]

    @property
    def ship_type_name(self):
        return self._ship_type_name

    @ship_type_name.setter
    def ship_type_name(self, esi: dict):
        self._ship_type_name = esi["name"]

    @property
    def ship_group_id(self):
        return self._ship_group_id

    @ship_group_id.setter
    def ship_group_id(self, esi: dict):
        self._ship_group_id = esi["group_id"]

    @property
    def ship_group_name(self):
        return self._ship_group_name

    @ship_group_name.setter
    def ship_group_name(self, esi: dict):
        self._ship_group_name = esi["name"]

    @property
    def ship_category_id(self):
        return self._ship_category_id

    @ship_category_id.setter
    def ship_category_id(self, esi: dict):
        self._ship_category_id = esi["category_id"]

    @property
    def ship_category_name(self):
        return self._ship_category_name

    @ship_category_name.setter
    def ship_category_name(self, esi: dict):
        self._ship_category_name = esi["name"]


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
