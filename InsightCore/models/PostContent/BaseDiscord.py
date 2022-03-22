from dataclasses import dataclass
from .BasePostContent import BasePostContent


@dataclass
class BaseDiscord(BasePostContent):
    content: str = ""

    def generate_payload(self):
        raise NotImplementedError

    def get_payload(self) -> dict:
        self.generate_payload()
        return {
            "content": self.content
        }
