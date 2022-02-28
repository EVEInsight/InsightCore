from dataclasses import dataclass, asdict, fields
from core.models.BaseModel import BaseModel
from .Config import Config
from .Filter import Filter
from pymongo.collection import ObjectId


@dataclass
class Stream(BaseModel):
    config: Config
    filter: Filter
    _id: str = None

    @classmethod
    def from_json(cls, dct: dict):
        """Returns an instance of class from a json dictionary

        :param dct: Dictionary returned from the to_json() method
        :return: An instance of the class
        :rtype: Stream
        """
        s = super().from_json(dct)
        if isinstance(s._id, ObjectId):
            s._id = str(s._id)
        s.config = Config.from_json(dct["config"])
        s.filter = Filter.from_json(dct["filter"])
        return s
