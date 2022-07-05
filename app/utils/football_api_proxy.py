import os
import threading

from ratelimiter import RateLimiter
import requests
from requests.models import Response


class Proxy:

    _instance = None
    _lock = threading.Lock()
    client = None
    headers = {'X-Auth-Token': os.getenv('FOOTBALL_KEY')}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                # another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(Proxy, cls).__new__(cls)

        return cls._instance

    def __init__(cls):
        if cls._instance.client is None:
            cls.client = requests

    @RateLimiter(max_calls=10, period=60)
    def get(cls, url: str) -> Response:
        return cls.client.get(url, headers=cls.headers)

