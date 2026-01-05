from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("auth/", include("users.urls")),
                path("social/posts/", include("posts.urls")),
                path("social/", include("interactions.urls")),
            ]
        ),
    ),
]
