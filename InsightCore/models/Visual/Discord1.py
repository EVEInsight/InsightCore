from dataclasses import dataclass
from .BaseDiscord import BaseDiscord


@dataclass
class Discord1(BaseDiscord):
    @classmethod
    def get_visual_id(cls):
        return 1

    def get_payload(self) -> dict:
        return {
            "content": self.mail.zk_url
        }
