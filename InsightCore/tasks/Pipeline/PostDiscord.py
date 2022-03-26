from InsightCore.tasks.BaseTasks.InsightCoreTask import InsightCoreTask
from InsightCore.models.Visual import BaseDiscord
import requests
from ESICelery.utils.RequestHeaders import RequestHeaders


class PostDiscord(InsightCoreTask):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 60
    retry_backoff_max = 600
    retry_jitter = False

    def run(self, post_json) -> None:
        p = BaseDiscord.from_json_subclass(post_json)
        try:
            resp = requests.post(url=p.stream.post.url, json=p.get_payload(), headers=RequestHeaders.get_headers(),
                                 timeout=15, verify=True)
            if 200 <= resp.status_code < 300:
                return
            elif resp.status_code in [401, 403, 404]:
                pass  # delete feed
            elif resp.status_code == 429:  # error limited
                pass  # set error limit
            elif 400 <= resp.status_code < 600:
                pass  # assume +1 to error limit
            else:
                pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        return
