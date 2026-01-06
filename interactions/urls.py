from rest_framework.routers import DefaultRouter

from interactions.views import PostInteractionViewSet, UserInteractionViewSet

router = DefaultRouter()
router.register("posts", PostInteractionViewSet, basename="post-interactions")
router.register("users", UserInteractionViewSet, basename="user-interactions")

urlpatterns = router.urls
