from dataclasses import dataclass
from InsightCore.models.BaseModel import BaseModel


@dataclass
class MailVictim(BaseModel):
    """
    mail victim representing data for Insight parsed from ZK json and additional attributes resolved through ESI
    """
    # directly resolved through zk mail json - required
    damage_taken: int
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
    _ship_adjusted_price: float = None

    @property
    def affiliation_name(self):
        """Returns the name of the largest affiliation the entity belongs to.
        Ordering - whichever id is set first: faction > alliance > corporation

        :return: Name of the largest affiliation the entity belongs to or None if no affiliation.
        :rtype: str or None
        """
        if self.faction_id:
            return self.faction_name
        elif self.alliance_id:
            return self.alliance_name
        elif self.corporation_id:
            return self.corporation_name
        else:
            return None

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
    def faction_name(self):
        """Set through ESI factions list call.

        :return: Faction name - optional
        :rtype: str or None
        """
        return self._faction_name

    @faction_name.setter
    def faction_name(self, esi: list):
        """Set through ESI factions list call.

        :param esi: ESI response list. ESI is required to return this value.
        """
        for f in esi:
            if f.get("faction_id") == self.faction_id:
                self._faction_name = f.get("name")

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

    @property
    def ship_adjusted_price(self):
        """Set through ESI prices list call.

        :return: Adjusted price if available else returns 0
        :rtype: float
        """
        return self._ship_adjusted_price if self._ship_adjusted_price is not None else 0

    @ship_adjusted_price.setter
    def ship_adjusted_price(self, esi: list):
        """Set through ESI prices list call.

        :param esi: ESI response list. ESI is required to return this value.
        """
        for t in esi:
            if t.get("type_id") == self.ship_type_id:
                self._ship_adjusted_price = t.get("adjusted_price")


@dataclass
class RedisQVictim(MailVictim):
    @classmethod
    def from_json(cls, dct: dict):
        d = dct
        d = {
            "damage_taken":     d["damage_taken"],
            "alliance_id":      d.get("alliance_id"),
            "character_id":     d.get("character_id"),
            "corporation_id":   d.get("corporation_id"),
            "faction_id":       d.get("faction_id"),
            "ship_type_id":     d.get("ship_type_id"),
            "position_x":       d.get("position", {}).get("x"),
            "position_y":       d.get("position", {}).get("y"),
            "position_z":       d.get("position", {}).get("z"),
        }
        return super().from_json(d)
