from InsightCore.CeleryApps import InsightCoreWorker
from InsightCore.tasks.API import CreateModifyStream
from InsightCore.models.Stream import *


def main():
    InsightCoreWorker.create_class()

    p = DiscordPost(url="http://localhost/id1", running=True)
    f = Filter()
    f.attacker_character_ids_include = ["*"]
    f.attacker_corporation_ids_include = ["*"]
    f.attacker_alliance_ids_include = ["*"]
    f.victim_character_ids_include = ["*"]
    f.victim_corporation_ids_include = ["*"]
    f.victim_alliance_ids_include = ["*"]
    f.system_ranges_gate_include = [SystemRangeGate(30002537, 5)]  # Amamake
    s = Stream(filter=f, post=p)
    returned_stream = CreateModifyStream().delay(stream_json=s.to_json()).wait(timeout=5)
    print(returned_stream)


if __name__ == '__main__':
    main()
