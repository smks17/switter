from django.middleware.cache import CacheMiddleware
from django.core.cache import cache


class CostumeCacheMiddleware(CacheMiddleware):
    def process_request(self, request):
        if self.should_cache_request(request):
            if request.GET.get("reload") != "true":
                return super().process_request(request)
            key = self._get_cache_key(request)
            if key:
                cache.delete(key)
        return None

    def should_cache_request(self, request):
        return request.method == "GET" and not request.user.is_authenticated

    def process_response(self, request, response):
        return super().process_response(request, response)

    def _get_cache_key(self, request):
        key = None
        try:
            key = cache.get(request)
        except Exception:
            pass
        return key
