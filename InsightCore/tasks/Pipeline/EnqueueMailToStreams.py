from InsightCore.models.Stream.Stream import Stream
from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from pymongo.collection import Collection
from InsightCore.tasks.Pipeline.StreamFiltersStage1 import StreamFiltersStage1


class EnqueueMailToStreams(InsightCoreTask):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 60
    retry_backoff_max = 600
    retry_jitter = False

    def run(self, mail_json) -> None:
        """Enqueue all ESI calls to resolve data that isn't present from ZK.

        :param self: Celery self reference required for retries.
        :param mail_json: json dictionary with Mail data after values are set from ESI
        :type mail_json: dict
        :rtype: None
        """
        streams: Collection = self.db.streams
        for s in streams.find({"post.running": True}):
            stream = Stream.from_json(s)
            stream_json = stream.to_json()
            StreamFiltersStage1().apply_async(kwargs={"mail_json": mail_json, "stream_json": stream_json},
                                              ignore_result=True)
