from InsightCore.models.Stream.Stream import Stream
from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from pymongo.collection import Collection


class CreateModifyStream(InsightCoreTask):
    def run(self, stream_json: dict) -> dict:
        """Create a new stream or modify the configuration of an existing stream. Returns the stream config.

        :param stream_json: json dictionary containing an Insight stream config.
        :type stream_json: dict
        :return: A dictionary containing the stream config.
        :rtype: dict
        """
        if not isinstance(stream_json, dict):
            raise TypeError("stream_json must be of type dictionary")
        s = Stream.from_json(stream_json)
        streams: Collection = self.db.streams
        with self.redis.lock("Lock-MongoDB", blocking_timeout=5, timeout=30):
            modified_stream = streams.find_one_and_update(filter={"post.url": s.post.url}, update={"$set": s.to_json()},
                                                          upsert=True, return_document=True)
            modified_stream.pop("_id")
            return Stream.from_json(modified_stream).to_json()
