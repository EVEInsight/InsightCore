from core.celery import app
from core.models.Stream.Stream import Stream
from core.tasks.BaseTasks.BaseTask import BaseTask
from pymongo.collection import Collection


@app.task(base=BaseTask)
def CreateStream(stream_json: dict) -> dict:
    """Create a new stream and return the stream ID.

    :param self: Celery self reference required for retries.
    :param stream_json: json dictionary containing an Insight stream config.
    :type stream_json: dict
    :return: A dictionary containing the ID of the created stream.
    :rtype: dict
    """
    if not isinstance(stream_json, dict):
        raise TypeError("stream_json must be of type dictionary")
    s = Stream.from_json(stream_json)
    stream_json = s.to_mongodb_json()

    streams: Collection = CreateStream.db.streams
    result = streams.insert_one(stream_json)

    return {"id": str(result.inserted_id)}

