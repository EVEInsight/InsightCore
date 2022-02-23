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
    system_name: str = None
    system_pos_x: float = None
    system_pos_y: float = None
    system_pos_z: float = None
    constellation_id: int = None
    constellation_name: str = None
    region_id: int = None
    region_name: str = None

    # additional vars parsed
    final_blow_attacker: MailAttacker = None

    # utility vars
    parsed_time: datetime = None

    def __init__(self, dct: dict):
        for k, v in dct.items():
            if k == "attackers":
                for a in v:
                    self.attackers = []
                    attacker = MailAttacker.from_json(a)
                    self.attackers.append(attacker)
                    if attacker.final_blow:
                        self.final_blow_attacker = attacker
            elif k == "victim":
                setattr(self, k, MailVictim.from_json(v))
            elif k == "final_blow_attacker":
                continue
            elif k == "killmail_time" or k == "parsed_time":
                setattr(self, k, dtparse(v))
            else:
                setattr(self, k, v)
        self.parsed_time = datetime.utcnow()

    def to_json(self) -> dict:
        d = asdict(self)
        d["killmail_time"] = str(d["killmail_time"])
        d["parsed_time"] = str(d["parsed_time"])
        return d

    @classmethod
    def from_json(cls, dct):
        return cls(dct)


@dataclass(init=False)
class RedisQMail(Mail):
    def __init__(self, dct: dict):
        d = dct.get("package")
        setattr(self, "id",                 d["killmail"]["killmail_id"])
        setattr(self, "killmail_time",      dtparse(d["killmail"]["killmail_time"]))
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
            if attacker.final_blow:
                self.final_blow_attacker = attacker

        self.parsed_time = datetime.utcnow()

    @classmethod
    def from_json(cls, dct: dict):
        return cls(dct)


