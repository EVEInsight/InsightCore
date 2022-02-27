import platform
import requests
import os


class RequestHeaders(object):
    @classmethod
    def get_email(cls):
        try:
            return os.environ["HeaderEmail"]
        except KeyError as ex:
            print("Missing 'HeaderEmail' env variable. Please set this variable to your email address so ESI and ZK "
                  "APIs can contact you if there are problems.")
            raise ex

    @classmethod
    def get_headers(cls) -> dict:
        h = {"Accept":      "application/json",
             "From":        cls.get_email(),
             "Maintainer":  "maintainers@eveinsight.net",
             "User-Agent":  f"InsightCore (https://github.com/EVEInsight/InsightCore) "
                            f"Python/{platform.python_version()} "
                            f"Requests/{requests.__version__}"}
        return h
