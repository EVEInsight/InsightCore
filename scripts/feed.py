from InsightCore.CeleryApps import InsightCoreWorker
from InsightCore.tasks.API import CreateStream
from InsightCore.models.Stream import *


def main():
    InsightCoreWorker.create_class()

    d = DiscordPostConfig(url="http://localhost", running=True)
    f = Filter()
    f.attacker_character_ids_include = ["*"]
    f.attacker_corporation_ids_include = ["*"]
    f.attacker_alliance_ids_include = ["*"]
    f.victim_character_ids_include = ["*"]
    f.victim_corporation_ids_include = ["*"]
    f.victim_alliance_ids_include = ["*"]
    f.system_ranges_gate_include = [SystemRangeGate(30002537, 5)]  # Amamake
    s = Stream(discord_post_configs=[d], filter=f)
    s_json = s.to_mongodb_json()
    CreateStream().delay(stream_json=s.to_mongodb_json()).wait(timeout=5)


if __name__ == '__main__':
    main()
