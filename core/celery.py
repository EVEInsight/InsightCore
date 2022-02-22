from celery import Celery


app = Celery("InsightCore")
app.config_from_object("core.celeryconfig")


def main():
    """entry point to celery app"""
    app.start()


if __name__ == '__main__':
    main()
