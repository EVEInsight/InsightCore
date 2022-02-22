from project.celery import app
import time


@app.task
def ProcessMailRedisQ(mail) -> None:
    """
    get mail using RedisQ
    :rtype: None
    """
    print(mail)
    return
