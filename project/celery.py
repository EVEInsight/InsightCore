from celery import Celery


app = Celery("InsightTasks")
app.config_from_object("project.celeryconfig")


def main():
    """entry point to celery app"""
    app.start()


if __name__ == '__main__':
    main()
