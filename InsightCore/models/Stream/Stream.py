from dataclasses import dataclass, asdict, fields
from InsightCore.models.BaseModel import BaseModel
from .Config import Config
from .Filter import Filter
from pymongo.collection import ObjectId


@dataclass
class Stream(BaseModel):
    config: Config
    filter: Filter
    id: str = None

    @classmethod
    def from_json(cls, dct: dict):
        """Returns an instance of class from a json dictionary

        :param dct: Dictionary returned from the to_json() method
        :return: An instance of the class
        :rtype: Stream
        """
        stream_id = dct.pop("_id", None)
        s = super().from_json(dct)
        if stream_id is not None:
            s.id = str(stream_id)
        s.config = Config.from_json(dct["config"])
        s.filter = Filter.from_json(dct["filter"])
        return s

    def to_mongodb_json(self) -> dict:
        """Returns a json dictionary with ID removed for inserts / updates into mongodb.

        :return: Instance with id field removed.
        """
        d = self.to_json()
        d.pop("id", None)
        return d


