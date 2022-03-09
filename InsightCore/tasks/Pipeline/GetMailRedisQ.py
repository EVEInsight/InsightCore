import os
import time
import warnings
from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
import requests
import string
import random
from redis.exceptions import LockError
from .ProcessMailEnqueueESICalls import ProcessMailEnqueueESICalls
from .ProcessMailLoadFromESI import ProcessMailLoadFromESI
from ESICelery.utils.RequestHeaders import RequestHeaders


class GetMailRedisQ(InsightCoreTask):

    @classmethod
    def get_zk_redisq_url(cls) -> str:
        """ZK redisq url with unique queue id. Will always contain a unique ID regardless if env var 'ZKQueueID' is set

        :return: request URL for redisq with a unique queue_id
        :rtype: str
        """
        try:
            queue_id = os.environ["ZKQueueID"]
        except KeyError:
            queue_id = "".join(random.choice(string.ascii_lowercase) for x in range(15))
            w = f"'ZKQueueID' env variable is not set. Using a temporary random queue id '{queue_id}'"
            warnings.warn(w)
        return f"https://redisq.zkillboard.com/listen.php?queueID={queue_id}"

    def run(self) -> None:
        """Get a mail from RedisQ and queue up tasks to the mail processing tasks.
        Only one instance of this task will run regardless of process count as a lock is acquired through Redis.
        This task is invoked on regular intervals through celery beat configured in celeryconfig.py

        :rtype: None
        """
        try:
            with self.redis.lock("Lock-GetMailRedisQ", blocking_timeout=1, timeout=600):
                try:
                    resp = requests.get(self.get_zk_redisq_url(), headers=RequestHeaders.get_headers(), timeout=15,
                                        verify=True)
                    if resp.status_code == 200:
                        data = resp.json()
                        try:
                            if data.get("package") is not None:
                                mail_id = data["package"]["killID"]  # test for id otherwise raise key error
                                ProcessMailEnqueueESICalls().apply_async(kwargs={"mail_json": data}, ignore_result=True)
                                ProcessMailLoadFromESI().apply_async(kwargs={"mail_json": data}, ignore_result=True)
                                return
                            else:
                                return
                        except KeyError:
                            return
                    elif resp.status_code == 429:  # error limited
                        warnings.warn("RedisQ error limited. Are multiple processes from the same IP calling RedisQ?")
                        time.sleep(600)
                    elif 400 <= resp.status_code < 500:
                        print(f"GetMailRedisQ.\nGot error f{resp.status_code}"
                              f"\n\nHeaders: {resp.headers}\n\nBody:{resp.text}")
                        time.sleep(300)
                    else:
                        time.sleep(120)
                except requests.exceptions.Timeout:
                    time.sleep(60)
                except requests.exceptions.ConnectionError:
                    warnings.warn("Unable to connect to RedisQ. Is there a DNS or connection problem?")
        except LockError:
            return
