import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from .MailAttacker import MailAttacker
from .MailVictim import MailVictim


@dataclass
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
    system_name: str = ""
    constellation_id: int = None
    constellation_name: str = ""
    region_id: int = None
    region_name: str = ""

    # utility vars
    parsed_time: datetime = datetime.utcnow()

    def json_encode(self):
        d = asdict(self)
        d["killmail_time"] = str(d["killmail_time"])
        d["parsed_time"] = str(d["parsed_time"])
        return json.dumps(d)

    @classmethod
    def json_decode_from_zk(cls, dct):
        d = dct.get("package")
        return cls(id=d["killmail"]["killmail_id"],
                   killmail_time=datetime.strptime(d["killmail"]["killmail_time"], "%Y-%m-%dT%XZ"),
                   system_id=d["killmail"]["solar_system_id"],
                   zkb_locationID=d["zkb"]["locationID"],
                   zkb_hash=d["zkb"]["hash"],
                   zkb_fittedValue=d["zkb"]["fittedValue"],
                   zkb_droppedValue=d["zkb"]["droppedValue"],
                   zkb_destroyedValue=d["zkb"]["destroyedValue"],
                   zkb_totalValue=d["zkb"]["totalValue"],
                   zkb_points=d["zkb"]["points"],
                   zkb_npc=d["zkb"]["npc"],
                   zkb_solo=d["zkb"]["solo"],
                   zkb_awox=d["zkb"]["awox"],
                   zkb_href=d["zkb"]["href"],
                   victim=MailVictim.json_decode_from_zk(dct),
                   attackers=MailAttacker.json_decode_multi_from_zk(dct)
                   )


