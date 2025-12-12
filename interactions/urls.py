from interactions.views import (
    CommentViewSet,
    FollowViewSet,
    LikeViewSet,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", LikeViewSet, "likes")
router.register("", CommentViewSet, "comments")
router.register("", FollowViewSet, "follow")

urlpatterns = router.urls
