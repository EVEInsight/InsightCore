from InsightCore.CeleryApps import InsightCoreWorker, InsightCoreBeat
import os
import sys


def main():
    if "--beat" in sys.argv:
        celery_server = InsightCoreBeat
    else:
        celery_server = InsightCoreWorker
    try:
        c = celery_server(os.environ["BrokerUser"], os.environ["BrokerPassword"], os.environ["BrokerHost"],
                          int(os.environ["BrokerPort"]), os.environ["BrokerVhost"],
                          os.environ["ResultBackendUser"], os.environ["ResultBackendPassword"],
                          os.environ["ResultBackendHost"],
                          int(os.environ["ResultBackendPort"]), int(os.environ["ResultBackendDb"]),
                          os.environ["HeaderEmail"])
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
