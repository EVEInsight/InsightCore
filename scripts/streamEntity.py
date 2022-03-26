from InsightCore.CeleryApps import InsightCoreWorker
from InsightCore.tasks.API import CreateModifyStream
from InsightCore.models.Stream import *
import os


def main():
    InsightCoreWorker.create_class()

    p = DiscordPost(url=os.environ["URL"], visual_id=int(os.environ["VISUAL_ID"]))
    f = Filter()
    f.attacker_character_ids_include = ["*"]
    f.attacker_corporation_ids_include = ["*"]
    f.attacker_alliance_ids_include = [99003581, 99005338, 1354830081]  # Frat, Horde, Goons
    f.attacker_faction_ids_include = ["*"]
    f.victim_character_ids_include = ["*"]
    f.victim_corporation_ids_include = ["*"]
    f.victim_alliance_ids_include = [99003581, 99005338, 1354830081]  # Frat, Horde, Goons
    f.victim_faction_ids_include = ["*"]
    f.operator_attacker_victim_and = False # set false to show both kills and losses. Setting this to true only tracks one
    s = Stream(filter=f, post=p)
    returned_stream = CreateModifyStream().delay(stream_json=s.to_json()).wait(timeout=5)
    print(returned_stream)


if __name__ == '__main__':
    main()
