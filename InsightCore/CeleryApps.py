from ESICelery.CeleryApps import CeleryWorker, CeleryBeat
from InsightCore.tasks.Pipeline import *
from InsightCore.tasks.API import *
import os


class InsightCoreWorker(CeleryWorker):
    def tasks_to_register(self):
        yield from super().tasks_to_register()
        yield GetMailRedisQ(), "PipelineGetMailRedisQ"
        yield ProcessMailEnqueueESICalls(), "PipelineProcessMailEnqueueESICalls"
        yield ProcessMailLoadFromESI(), "PipelineProcessMailLoadFromESI"
        yield EnqueueMailToStreams(), "PipelineEnqueueMailToStreams"
        yield StreamFiltersStage1(), "PipelineStreamFiltersStage1"
        yield StreamFiltersStage2(), "PipelineStreamFiltersStage2"
        yield CreateStream(), "ApiCreateStream"

    @classmethod
    def create_class(cls):
        """helper function to create an instance of the celery app reading the config variables from env variables.

        :return: An instance of the celery app wrapper class
        :rtype: cls
        """
        c = cls(os.environ["BrokerUser"], os.environ["BrokerPassword"], os.environ["BrokerHost"],
                int(os.environ["BrokerPort"]), os.environ["BrokerVhost"],
                os.environ["ResultBackendUser"], os.environ["ResultBackendPassword"], os.environ["ResultBackendHost"],
                int(os.environ["ResultBackendPort"]), int(os.environ["ResultBackendDb"]),
                os.environ["HeaderEmail"])
        return c


class InsightCoreBeat(CeleryBeat, InsightCoreWorker):
    def tasks_to_register(self):
        yield GetMailRedisQ(), "PipelineGetMailRedisQ"
