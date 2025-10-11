from django.db import models
from django.contrib.auth.models import User

from switter.settings import MEDIA_PATH


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"


class MediaPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(
        upload_to=MEDIA_PATH
    )  # TODO: define upload to variable in settings
    # type_media =
