import os
import pymongo
from urllib.parse import quote_plus
from pymongo.database import Database
from ESICelery.tasks.BaseTasks.BaseTask import BaseTask


class InsightCoreTask(BaseTask):
    _db: pymongo.database.Database = None

    @property
    def db(self) -> pymongo.database.Database:
        if self._db is None:
            user = os.environ["DbUser"]
            password = os.environ["DbPassword"]
            db = os.environ["DbName"]
            host = os.environ["DbHost"]
            port = int(os.environ["DbPort"])
            uri = f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}"
            client = pymongo.MongoClient(uri, maxPoolSize=10)
            self._db = client[db]
        return self._db
