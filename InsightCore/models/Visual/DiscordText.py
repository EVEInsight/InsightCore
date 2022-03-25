from dataclasses import dataclass
from .BaseDiscord import BaseDiscord


@dataclass
class DiscordText(BaseDiscord):
    @classmethod
    def get_visual_id(cls):
        return 1

    def generate_payload(self):
        self.content = f"https://zkillboard.com/kill/{self.mail.id}/"
