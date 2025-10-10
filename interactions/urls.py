from django.urls import path

from interactions.views import add_comment_view, toggle_like_view


urlpatterns = [
    path("<int:post_id>/like", toggle_like_view),
    path("<int:post_id>/comment", add_comment_view),
]
