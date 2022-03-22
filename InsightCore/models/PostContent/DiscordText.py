from dataclasses import dataclass
from .BaseDiscord import BaseDiscord


@dataclass
class DiscordText(BaseDiscord):
    def generate_payload(self):
        self.content = f"https://zkillboard.com/kill/{self.mail.id}/"
