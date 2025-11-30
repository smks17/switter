from django.urls import path

from posts.views import (
    get_home_posts_view,
    get_my_posts_view,
    create_post_view,
    get_post_details_view,
    download_media,
)


urlpatterns = [
    path("", get_home_posts_view, name="get home posts"),
    path("", create_post_view, name="create new post"),
    path("me/", get_my_posts_view, name="get my posts"),
    path("<int:post_id>/", get_post_details_view, name="post detail"),
    path("media/<int:file_id>/", download_media, name="download media"),
]
