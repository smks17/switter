from django.urls import path

from posts.views import (
    get_all_posts_view,
    get_my_posts_view,
    create_post_view,
    get_post_details_view,
)


urlpatterns = [
    path("", get_all_posts_view, name="get all posts"),
    path("me", get_my_posts_view, name="get all posts"),
    path("new", create_post_view, name="create new post"),
    path("<int:post_id>", get_post_details_view, name="post detail"),
]
