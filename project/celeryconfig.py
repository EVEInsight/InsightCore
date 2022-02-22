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
include = ["project.tasks.pipeline.GetMailRedisQ",
           "project.tasks.pipeline.ProcessMail",
           "project.tasks.pipeline.EnqueueMailToActiveChannels"]
task_default_queue = "CeleryDefault"
task_routes = {"project.tasks.pipeline.GetMailRedisQ.*": {"queue": "GetMailRedisQ"},
               "project.tasks.pipeline.ProcessMail.*": {"queue": "ProcessMail"},
               "project.tasks.pipeline.EnqueueMailToActiveChannels.*": {"queue": "EnqueueMailToActiveChannels"},
               }
beat_schedule = {
    "pull mail redisq": {
        'task': 'project.tasks.pipeline.GetMailRedisQ.GetMailRedisQ',
        'schedule': 1
    },
}
