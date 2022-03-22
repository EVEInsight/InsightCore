from ESICelery.CeleryApps import CeleryWorker, CeleryBeat
from InsightCore.tasks.Pipeline import *
from InsightCore.tasks.API import *


class InsightCoreWorker(CeleryWorker):
    def tasks_to_register(self):
        yield from super().tasks_to_register()
        yield GetMailRedisQ(), "PipelineGetMailRedisQ"
        yield ProcessMailEnqueueESICalls(), "PipelineProcessMailEnqueueESICalls"
        yield ProcessMailLoadFromESI(), "PipelineProcessMailLoadFromESI"
        yield EnqueueMailToStreams(), "PipelineEnqueueMailToStreams"
        yield StreamFiltersStage1(), "PipelineStreamFiltersStage1"
        yield StreamFiltersStage2(), "PipelineStreamFiltersStage2"
        yield CreateModifyStream(), "ApiCreateModifyStream"
        yield PostDiscord(), "PipelinePostDiscord"


class InsightCoreBeat(CeleryBeat):
    def tasks_to_register(self):
        yield GetMailRedisQ(), "PipelineGetMailRedisQ"
