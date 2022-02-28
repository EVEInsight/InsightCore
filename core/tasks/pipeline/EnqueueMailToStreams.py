from core.celery import app
from core.models.Stream.Stream import Stream
from core.models.Mail.Mail import Mail
from core.tasks.BaseTasks.BaseTask import BaseTask
from pymongo.collection import Collection
from core.tasks.pipeline.StreamFiltersStage1 import StreamFiltersStage1


@app.task(base=BaseTask, bind=True, max_retries=5, default_retry_delay=1, autoretry_for=(Exception,))
def EnqueueMailToStreams(self, mail_json) -> None:
    """Enqueue all ESI calls to resolve data that isn't present from ZK.

    :param self: Celery self reference required for retries.
    :param mail_json: json dictionary with Mail data after values are set from ESI
    :type mail_json: dict
    :rtype: None
    """
    streams: Collection = self.db.streams
    m = Mail.from_json(mail_json)
    for s in streams.find({"config.running": True}):
        stream = Stream.from_json(s)
        stream_json = stream.to_json()
        StreamFiltersStage1.apply_async(kwargs={"mail_json": mail_json, "stream_json": stream_json}, ignore_result=True)

