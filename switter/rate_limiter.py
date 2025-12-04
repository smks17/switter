import datetime
import os
import time

from django.http import HttpResponse
from django_redis import get_redis_connection


class RateLimiterMiddleware:
    MAX_RATE_LIMIT = os.environ.get("RATE_LIMIT", 1000)  # per day
    WINDOW = int(datetime.timedelta(days=1).total_seconds())

    def __init__(self, get_response):
        self.get_response = get_response
        self.redis = get_redis_connection("rate_limiter")

    def _get_client_ip(self, request):
        if x_forwarded_for := request.META.get("HTTP_X_FORWARDED_FOR"):
            return x_forwarded_for.split(",")[0]
        return request.META["REMOTE_ADDR"]

    def __call__(self, request):
        ip = self._get_client_ip(request)
        key = f"rate:{ip}"
        now = int(time.time())

        self.redis.zremrangebyscore(key, 0, (now - self.WINDOW))
        num_requests = self.redis.zcard(key)
        if num_requests > self.MAX_RATE_LIMIT:
            return HttpResponse("Too many request", status=429)
        self.redis.zadd(key, {now: now})
        self.redis.expire(key, self.WINDOW)

        return self.get_response(request)
