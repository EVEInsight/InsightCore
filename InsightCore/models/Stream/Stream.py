from dataclasses import dataclass, field, asdict
from InsightCore.models.BaseModel import BaseModel
from .Filter import Filter
from .Post import Post, DiscordPost


@dataclass
class Stream(BaseModel):
    filter: Filter
    post: Post

    @classmethod
    def from_json(cls, dct: dict):
        """Returns an instance of class from a json dictionary

        :param dct: Dictionary returned from the to_json() method
        :return: An instance of the class
        :rtype: Stream
        """
        s = super().from_json(dct)
        s.filter = Filter.from_json(dct["filter"])
        post_type = dct["post"]["visual_type"]
        if post_type == "discord":
            s.post = DiscordPost.from_json(dct["post"])
        else:
            raise ValueError("Unexpected post type")
        return s

