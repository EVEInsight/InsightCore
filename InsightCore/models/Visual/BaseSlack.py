from dataclasses import dataclass
from .BaseVisual import BaseVisual


@dataclass
class BaseSlack(BaseVisual):
    content: str = ""

    @classmethod
    def get_visual_type(cls):
        return "slack"

    def get_payload(self) -> dict:
        self.generate_payload()
        return {
            "content": self.content
        }
