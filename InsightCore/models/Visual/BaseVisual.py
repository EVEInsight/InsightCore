from dataclasses import dataclass, field
from InsightCore.models.BaseModel import BaseModel
from InsightCore.models.Mail import Mail, MailAttacker
from InsightCore.models.Stream import Stream
from InsightCore.exceptions.models import SubclassNotFound


@dataclass
class BaseVisual(BaseModel):
    mail: Mail
    stream: Stream
    visual_id: int
    visual_type: str
    filtered_attackers: list[MailAttacker] = field(default_factory=list)
    filtered_system_id: int = None
    filtered_system_name: str = None
    filtered_system_gate_distance: int = None
    filtered_system_lightyear_distance: float = None

    @classmethod
    def get_visual_id(cls):
        """Visual ID for the visual

        :return: Visual ID
        :rtype: int
        """
        raise NotImplementedError

    @classmethod
    def get_visual_type(cls):
        """Visual category name for the visual

        :return: Visual type
        :rtype: str
        """
        raise NotImplementedError

    @classmethod
    def from_json(cls, dct: dict):
        """Returns an instance of class from a json dictionary

        :param dct: Dictionary returned from the to_json() method
        :return: An instance of the class
        :rtype: BaseVisual
        """
        p = super().from_json(dct)
        p.mail = Mail.from_json(dct["mail"])
        p.stream = Stream.from_json(dct["stream"])
        p.attackers = [MailAttacker.from_json(a) for a in p.filtered_attackers]  # covert to class instances
        return p

    @classmethod
    def get_subclasses(cls):
        for c in cls.__subclasses__():
            yield c
            yield from c.get_subclasses()

    @classmethod
    def get_cls(cls, visual_type: str, visual_id: int):
        """Returns a subclass matching visual_type and visual_id

        :param visual_type: The visual string: discord, slack, etc.
        :param visual_id: The visual ID to generate.
        :return: A class type inherited from Visual matching visual_type and visual_id
        :raises SubclassNotFound: if the visual type and id do not match any subclasses.
        """
        for c in cls.get_subclasses():
            try:
                if c.get_visual_type() == visual_type and c.get_visual_id() == visual_id:
                    return c
            except NotImplementedError:  # received a base class so ignore it
                continue
        raise SubclassNotFound(f"No Visual class was found with type: {visual_type} and id: {visual_id}.")

    @classmethod
    def from_json_subclass(cls, dct: dict):
        """Returns instance of the subclass matching visual_type and visual_id

        :param dct: Dictionary returned from the to_json() method for a Visual class.
        :return: A class object inherited from Visual matching visual_type and visual_id
        :rtype: BaseVisual
        :raises SubclassNotFound: if the visual type and id do not match any subclasses.
        """
        return cls.get_cls(visual_type=dct["visual_type"], visual_id=dct["visual_id"]).from_json(dct)

    def generate_payload(self):
        raise NotImplementedError

    def get_payload(self) -> dict:
        raise NotImplementedError

