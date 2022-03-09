from ESICelery.CeleryApps import CeleryWorker, CeleryBeat
from InsightCore.tasks.Pipeline import *
from InsightCore.tasks.API import *
import sys
import os


class CeleryLauncher(object):
    @classmethod
    def tasks(cls):
        yield GetMailRedisQ()
        yield ProcessMailEnqueueESICalls()
        yield ProcessMailLoadFromESI()
        yield EnqueueMailToStreams()
        yield StreamFiltersStage1()
        yield StreamFiltersStage2()
        yield CreateStream()

    @classmethod
    def run(cls):
        if "--beat" in sys.argv:
            celery_server = CeleryBeat
        else:
            celery_server = CeleryWorker
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
        for t in cls.tasks():
            c.register_task(t)
            c.register_additional_queue(t.name)
            c.register_task_route(t.name, t.name)
        if isinstance(c, CeleryBeat):
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
