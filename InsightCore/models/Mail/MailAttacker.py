from dataclasses import dataclass
from InsightCore.models.BaseModel import BaseModel
from InsightCore.utils import Links


@dataclass
class MailAttacker(BaseModel):
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

    # unresolved ship weapon type info requiring api call
    _weapon_type_name: str = None
    _weapon_group_id: int = None
    _weapon_group_name: str = None
    _weapon_category_id: int = None
    _weapon_category_name: str = None
    _weapon_adjusted_price: float = None

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
    def character_zk_url(self) -> str:
        """

        :return: ZK url for character profile or an empty string if character_is is None
        """
        return Links.zk_character_url(self.character_id) if self.character_id else ""

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

        :param esi: ESI response list. ESI may return this value.
        """
        for t in esi:
            if t.get("type_id") == self.ship_type_id:
                self._ship_adjusted_price = t.get("adjusted_price")

    @property
    def weapon_type_name(self):
        return self._weapon_type_name

    @weapon_type_name.setter
    def weapon_type_name(self, esi: dict):
        self._weapon_type_name = esi["name"]

    @property
    def weapon_group_id(self):
        return self._weapon_group_id

    @weapon_group_id.setter
    def weapon_group_id(self, esi: dict):
        self._weapon_group_id = esi["group_id"]

    @property
    def weapon_group_name(self):
        return self._weapon_group_name

    @weapon_group_name.setter
    def weapon_group_name(self, esi: dict):
        self._weapon_group_name = esi["name"]

    @property
    def weapon_category_id(self):
        return self._weapon_category_id

    @weapon_category_id.setter
    def weapon_category_id(self, esi: dict):
        self._weapon_category_id = esi["category_id"]

    @property
    def weapon_category_name(self):
        return self._weapon_category_name

    @weapon_category_name.setter
    def weapon_category_name(self, esi: dict):
        self._weapon_category_name = esi["name"]

    @property
    def weapon_adjusted_price(self):
        """Set through ESI prices list call.

        :return: Adjusted price if available else returns 0
        :rtype: float
        """
        return self._weapon_adjusted_price if self._weapon_adjusted_price is not None else 0

    @weapon_adjusted_price.setter
    def weapon_adjusted_price(self, esi: list):
        """Set through ESI prices list call.

        :param esi: ESI response list. ESI may return this value.
        """
        for t in esi:
            if t.get("type_id") == self.weapon_type_id:
                self._weapon_adjusted_price = t.get("adjusted_price")


@dataclass
class RedisQMailAttacker(MailAttacker):
    @classmethod
    def from_json(cls, dct: dict):
        d = dct
        d = {
            "damage_done":      d["damage_done"],
            "final_blow":       d["final_blow"],
            "security_status":  d["security_status"],
            "alliance_id":      d.get("alliance_id"),
            "character_id":     d.get("character_id"),
            "corporation_id":   d.get("corporation_id"),
            "faction_id":       d.get("faction_id"),
            "ship_type_id":     d.get("ship_type_id"),
            "weapon_type_id":   d.get("weapon_type_id")
        }
        return super().from_json(d)
