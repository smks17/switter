from rest_framework import serializers

from interactions.models import Comment, FollowLinks, Like


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    post_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "username", "post_id"]


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="user.username", read_only=True)
    post_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "author_username", "post_id"]


class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(
        source="follower.username", read_only=True
    )
    following_username = serializers.CharField(
        source="following.username", read_only=True
    )

    class Meta:
        model = FollowLinks
        fields = [
            "id",
            "follower_username",
            "following_username",
        ]
