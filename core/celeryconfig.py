import os


def get_broker_url():
    """read env vars for rabbit mq to general connect url"""
    user = os.environ["MessageQueueUser"]
    password = os.environ["MessageQueuePassword"]
    host = os.environ["MessageQueueHost"]
    port = os.environ["MessageQueuePort"]
    vhost = os.environ["MessageQueueVhost"]
    return f"amqp://{user}:{password}@{host}:{port}/{vhost}"


broker_url = get_broker_url()
include = ["core.tasks.pipeline.GetMailRedisQ",
           "core.tasks.pipeline.ProcessMail",
           "core.tasks.pipeline.EnqueueMailToActiveChannels"]
task_default_queue = "CeleryDefault"
task_routes = {"core.tasks.pipeline.GetMailRedisQ.*": {"queue": "GetMailRedisQ"},
               "core.tasks.pipeline.ProcessMail.*": {"queue": "ProcessMail"},
               "core.tasks.pipeline.EnqueueMailToActiveChannels.*": {"queue": "EnqueueMailToActiveChannels"},
               }
beat_schedule = {
    "pull mail redisq": {
        'task': 'core.tasks.pipeline.GetMailRedisQ.GetMailRedisQ',
        'schedule': 1
    },
}
