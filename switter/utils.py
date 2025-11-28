from django.core.cache import cache
from functools import wraps


def create_user_cache(user_id, request_path):
    return f"{user_id}:{request_path}"


def user_cached(timeout=300):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not user or not user.is_authenticated:
                return view_func(request, *args, **kwargs)

            cache_key = create_user_cache(user.id, request.path)
            if request.GET.get("reload") != "true":
                cached_result = cache.get(cache_key)
                if cached_result:
                    return cached_result

            response = view_func(request, *args, **kwargs)

            cache.set(cache_key, response, timeout=timeout)

            return response

        return wrapper

    return decorator
