from InsightCore.CeleryApps import InsightCoreWorker, InsightCoreBeat
import os
import sys


def main():
    try:
        if "--beat" not in sys.argv:
            c = InsightCoreWorker.create_class()
        else:
            c = InsightCoreBeat.create_class()
    except KeyError as ex:
        print("Environmental variable is not set.")
        raise ex
    if isinstance(c, InsightCoreBeat):
        s = {"task": "GetMailRedisQ",
             "schedule": 0.5,
             "options": {
                 "ignore_result": True,
                 "expires": 2
             }
             }
        c.schedule_task("get-mail-redisq", s)
        c.start()
    else:
        c.start(max_concurrency=int(os.environ["MaxConcurrency"]))


if __name__ == '__main__':
    main()
