from rest_framework import serializers

from posts.models import MediaPost, Post


class MediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = MediaPost
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/api/social/posts/media/{obj.id}"


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "created_at",
            "author_username",
            "likes_count",
            "comments_count",
            "media",
        ]
