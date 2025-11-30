from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/social/posts/", include("posts.urls")),
    path("api/social/", include("interactions.urls")),
]
