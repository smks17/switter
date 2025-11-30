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

urlpatterns = []

# likes
urlpatterns += [
    path("posts/<int:post_id>/like/", toggle_like_view),
    path("users/me/likes/", my_likes_view),
]

# comments
urlpatterns += [
    path("posts/<int:post_id>/comment/", add_comment_view),
    path("users/me/comments/", my_comments_view),
]

# follow
urlpatterns += [
    path("users/<int:user_id>/follow/", follow_view),
    path("users/me/followers/", my_followers_view),
    path("users/<int:user_id>/followers/", followers_view),
    path("users/me/following/", my_followings_view),
    path("users/<int:user_id>/following/", followings_view),
]
