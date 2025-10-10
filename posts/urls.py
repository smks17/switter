from django.urls import path

from posts.views import get_all_posts_view, create_post_view


urlpatterns = [
    path("", get_all_posts_view, name="get all posts"),
    path("new", create_post_view, name="create new post"),
    # path("<int:pk>/", post_view, name="post handler"),
]
