from django.urls import path

from interactions.views import (
    add_comment_view,
    follow_view,
    followers_view,
    followings_view,
    my_comments_view,
    my_followers_view,
    my_followings_view,
    my_likes_view,
    toggle_like_view,
)


urlpatterns = [
    path("likes/<int:post_id>", toggle_like_view),
    path("comments/<int:post_id>", add_comment_view),
    path("likes/me", my_likes_view),
    path("comments/me", my_comments_view),
    path("follows/<int:user_id>", follow_view),
    path("followers/me", my_followers_view),
    path("followers/<int:user_id>", followers_view),
    path("followings/me", my_followings_view),
    path("followings/<int:user_id>", followings_view),
]
