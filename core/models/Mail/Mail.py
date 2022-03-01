from dataclasses import dataclass, field, asdict
from datetime import datetime
from .MailAttacker import MailAttacker, RedisQMailAttacker
from .MailVictim import MailVictim, RedisQVictim
from dateutil.parser import parse as dtparse


@dataclass(init=False)
class Mail:
    # directly resolved through zk mail json - required
    id: int
    killmail_time: datetime
    system_id: int

    zkb_locationID: int
    zkb_hash: str
    zkb_fittedValue: float
    zkb_droppedValue: float
    zkb_destroyedValue: float
    zkb_totalValue: float
    zkb_points: int
    zkb_npc: bool
    zkb_solo: bool
    zkb_awox: bool
    zkb_href: str
    victim: MailVictim
    attackers: list[MailAttacker] = field(default_factory=list)

    # unresolved system info requiring api calls
    _system_name: str = None
    _system_security_status: float = None
    _system_pos_x: float = None
    _system_pos_y: float = None
    _system_pos_z: float = None
    _constellation_id: int = None
    _constellation_name: str = None
    _region_id: int = None
    _region_name: str = None

    # utility vars
    parsed_time: datetime = None

    def __init__(self, dct: dict):
        for k, v in dct.items():
            if k == "attackers":
                self.attackers = []
                for a in v:
                    attacker = MailAttacker.from_json(a)
                    self.attackers.append(attacker)
            elif k == "victim":
                setattr(self, k, MailVictim.from_json(v))
            elif k == "_final_blow_attacker":
                continue
            elif k == "killmail_time" or k == "parsed_time":
                setattr(self, k, dtparse(v, ignoretz=True))
            else:
                setattr(self, k, v)
        self.parsed_time = datetime.utcnow()

    def to_json(self) -> dict:
        """Converts the class object to a json compatible dictionary

        :return: The json compatible dictionary of this object
        """
        d = asdict(self)
        d["killmail_time"] = str(d["killmail_time"])
        d["parsed_time"] = str(d["parsed_time"])
        return d

    @classmethod
    def from_json(cls, dct: dict):
        """Returns an instance of class from a json dictionary

        :param dct: Dictionary returned from the to_json() method
        :return: An instance of the class
        :rtype: Mail
        """
        return cls(dct)

    @property
    def system_name(self):
        """Set through ESI system info call.

        :return: System name - required
        :rtype: str
        """
        return self._system_name

    @system_name.setter
    def system_name(self, esi: dict):
        """Set through ESI system info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._system_name = esi["name"]

    @property
    def system_security_status(self):
        """Set through ESI system info call.

        :return: System security status - required
        :rtype: float
        """
        return self._system_security_status

    @system_security_status.setter
    def system_security_status(self, esi: dict):
        """Set through ESI system info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._system_security_status = esi["security_status"]

    @property
    def system_pos_x(self):
        """Set through ESI system info call.

        :return: System X position in the universe - required
        :rtype: float
        """
        return self._system_pos_x

    @system_pos_x.setter
    def system_pos_x(self, esi: dict):
        """Set through ESI system info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._system_pos_x = esi["position"]["x"]

    @property
    def system_pos_y(self):
        """Set through ESI system info call.

        :return: System Y position in the universe - required
        :rtype: float
        """
        return self._system_pos_y

    @system_pos_y.setter
    def system_pos_y(self, esi: dict):
        """Set through ESI system info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._system_pos_y = esi["position"]["y"]

    @property
    def system_pos_z(self):
        """Set through ESI system info call.

        :return: System Z position in the universe - required
        :rtype: float
        """
        return self._system_pos_z

    @system_pos_z.setter
    def system_pos_z(self, esi: dict):
        """Set through ESI system info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._system_pos_z = esi["position"]["z"]

    @property
    def constellation_id(self):
        """Set through ESI system info call.

        :return: Constellation ID - required
        :rtype: int
        """
        return self._constellation_id

    @constellation_id.setter
    def constellation_id(self, esi: dict):
        """Set through ESI system info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._constellation_id = esi["constellation_id"]

    @property
    def constellation_name(self):
        """Set through ESI constellation info call.

        :return: Constellation name - required
        :rtype: str
        """
        return self._constellation_name

    @constellation_name.setter
    def constellation_name(self, esi: dict):
        """Set through ESI constellation info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._constellation_name = esi["name"]

    @property
    def region_id(self):
        """Set through ESI constellation info call.

        :return: Region ID - required
        :rtype: int
        """
        return self._region_id

    @region_id.setter
    def region_id(self, esi: dict):
        """Set through ESI constellation info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._region_id = esi["region_id"]

    @property
    def region_name(self):
        """Set through ESI region info call.

        :return: Region name - required
        :rtype: str
        """
        return self._region_name

    @region_name.setter
    def region_name(self, esi: dict):
        """Set through ESI region info call.

        :param esi: ESI response dictionary. ESI is required to return this value.
        """
        self._region_name = esi["name"]

    @property
    def final_blow_attacker(self):
        """Dynamically gets the final_blow object

        :return: Attacker object with final_blow
        :rtype: MailAttacker or None
        """
        for a in self.attackers:
            if a.final_blow:
                return a
        return None

    @property
    def sorted_attackers_ship_adjusted_value(self):
        """Dynamically get attacker objects sorted in descending order by ship adjusted values.

        :return: Attacker objects sorted in descending order by ship adjusted values.
        :rtype: list
        """
        has_value = []
        no_value = []
        for a in self.attackers:
            if a.ship_adjusted_price is not None:
                has_value.append(a)
            else:
                no_value.append(a)
        return sorted(has_value, reverse=True, key=lambda x: x.ship_adjusted_price) + no_value

    @property
    def highest_attacker_ship_adjusted_value(self):
        """Get the attacker with highest ship adjusted value

        :return: Attacker object with highest ship adjusted value
        :rtype: MailAttacker or None
        """
        try:
            return self.sorted_attackers_ship_adjusted_value[0]
        except IndexError:
            return None

    @property
    def involved(self):
        """Dynamically get the involved count

        :return: Number of involved attackers
        :rtype: int
        """
        return len(self.attackers)


@dataclass(init=False)
class RedisQMail(Mail):
    def __init__(self, dct: dict):
        d = dct.get("package")
        setattr(self, "id",                 d["killmail"]["killmail_id"])
        setattr(self, "killmail_time",      dtparse(d["killmail"]["killmail_time"], ignoretz=True))
        setattr(self, "system_id",          d["killmail"]["solar_system_id"])
        setattr(self, "zkb_locationID",     d["zkb"]["locationID"])
        setattr(self, "zkb_hash",           d["zkb"]["hash"])
        setattr(self, "zkb_fittedValue",    d["zkb"]["fittedValue"])
        setattr(self, "zkb_droppedValue",   d["zkb"]["droppedValue"])
        setattr(self, "zkb_destroyedValue", d["zkb"]["destroyedValue"])
        setattr(self, "zkb_totalValue",     d["zkb"]["totalValue"])
        setattr(self, "zkb_points",         d["zkb"]["points"])
        setattr(self, "zkb_npc",            d["zkb"]["npc"])
        setattr(self, "zkb_solo",           d["zkb"]["solo"])
        setattr(self, "zkb_awox",           d["zkb"]["awox"])
        setattr(self, "zkb_href",           d["zkb"]["href"])
        setattr(self, "victim",             RedisQVictim.from_json(d["killmail"]["victim"]))
        self.attackers = []
        for a in d["killmail"]["attackers"]:
            attacker = RedisQMailAttacker.from_json(a)
            self.attackers.append(attacker)

        self.parsed_time = datetime.utcnow()

    @classmethod
    def from_json(cls, dct: dict):
        return cls(dct)
