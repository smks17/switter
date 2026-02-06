import json
from django.core.cache import cache
from rest_framework.response import Response
from functools import wraps

from switter.settings import USE_CACHE


def create_user_cache(user_id, request_path):
    return f"user:{user_id}:{request_path}"


def user_cached(timeout=300):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(obj, request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not USE_CACHE and (not user or not user.is_authenticated):
                return view_func(obj, request, *args, **kwargs)

            cache_key = create_user_cache(user.id, request.get_full_path())
            if request.GET.get("reload") != "true":
                cached_result = cache.get(cache_key)
                if cached_result:
                    return Response(json.loads(cached_result))

            response = view_func(obj, request, *args, **kwargs)

            if response.status_code == 200:
                cache.set(cache_key, json.dumps(response.data), timeout=timeout)

            return response

        return wrapper

    return decorator
