from InsightCore.CeleryApps import InsightCoreWorker
from InsightCore.tasks.API import CreateModifyStream
from InsightCore.models.Stream import *
import os


def main():
    InsightCoreWorker.create_class()

    p = DiscordPost(url=os.environ["URL"], visual_id=1)
    f = Filter()
    f.attacker_character_ids_include = ["*"]
    f.attacker_corporation_ids_include = ["*"]
    f.attacker_alliance_ids_include = ["*"]
    f.victim_character_ids_include = ["*"]
    f.victim_corporation_ids_include = ["*"]
    f.victim_alliance_ids_include = ["*"]
    f.km_min_totalValue = 0
    #f.system_ranges_gate_include = [SystemRangeGate(30002537, 25)]  # Amamake
    s = Stream(filter=f, post=p)
    returned_stream = CreateModifyStream().delay(stream_json=s.to_json()).wait(timeout=5)
    print(returned_stream)


if __name__ == '__main__':
    main()
