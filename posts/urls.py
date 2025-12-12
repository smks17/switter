from rest_framework.routers import DefaultRouter
from django.urls import path

from posts.views import PostViewSet, DownloadView


router = DefaultRouter()
router.register("", PostViewSet, "posts")
urlpatterns = router.urls + [
    path("media/<int:file_id>/", DownloadView.as_view(), name="download media"),
]
