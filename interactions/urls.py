from django.urls import path

from interactions.views import (
    add_comment_view,
    my_comments_view,
    my_likes_view,
    toggle_like_view,
)


urlpatterns = [
    path("<int:post_id>/like", toggle_like_view),
    path("<int:post_id>/comment", add_comment_view),
    path("likes/me", my_likes_view),
    path("comments/me", my_comments_view),
]
