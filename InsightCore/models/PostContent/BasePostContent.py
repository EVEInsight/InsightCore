from dataclasses import dataclass, field, asdict
from InsightCore.models.BaseModel import BaseModel
from InsightCore.models.Mail import Mail, MailAttacker
from InsightCore.models.Stream import Stream


@dataclass
class BasePostContent(BaseModel):
    mail: Mail
    stream: Stream
    filtered_attackers: list[MailAttacker] = field(default_factory=list)
    filtered_system_id: int = None
    filtered_system_name: str = None
    filtered_system_gate_distance: int = None
    filtered_system_lightyear_distance: float = None

    @classmethod
    def from_json(cls, dct: dict):
        """Returns an instance of class from a json dictionary

        :param dct: Dictionary returned from the to_json() method
        :return: An instance of the class
        :rtype: BasePostContent
        """
        p = super().from_json(dct)
        p.mail = Mail.from_json(dct["mail"])
        p.stream = Stream.from_json(dct["stream"])
        p.attackers = [MailAttacker.from_json(a) for a in p.filtered_attackers]  # covert to class instances
        return p

    def generate_payload(self):
        raise NotImplementedError

    def get_payload(self) -> dict:
        raise NotImplementedError

