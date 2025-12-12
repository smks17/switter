from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


from interactions.models import Comment, FollowLinks, Like
from interactions.serializer import CommentSerializer, FollowSerializer, LikeSerializer
from posts.models import Post


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all().select_related("author")
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["post"], url_path="posts/(?P<post_id>[^/.]+)/like", detail=False)
    def toggle_like(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"liked": False})
        return Response({"liked": True})

    @action(methods=["get"], url_path="posts/(?P<post_id>[^/.]+)/likes", detail=False)
    def get_post_like(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        likes = post.comments.select_related("user").order_by("-created_at")
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(methods=["get"], url_path="users/me/likes", detail=False)
    def my_likes(self, request):
        likes = Like.objects.filter(user=request.user).select_related("user", "post")
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(
        methods=["post"], url_path="posts/(?P<post_id>[^/.]+)/comment", detail=False
    )
    def add_comment(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post)
        return Response(serializer.data)

    @action(
        methods=["get"],
        url_path="posts/(?P<post_id>[^/.]+)/comments",
        detail=False,
    )
    def get_post_comments(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.select_related("user").order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(methods=["get"], url_path="users/me/comments", detail=False)
    def my_comments(self, request):
        comments = Comment.objects.filter(user=request.user).select_related(
            "user", "post"
        )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["post"], url_path="users/(?P<user_id>[^/.]+)/follow", detail=False)
    def toggle_follow(self, request, user_id=None):
        following_user = get_object_or_404(User, id=user_id)
        obj, created = FollowLinks.objects.get_or_create(
            follower=request.user, following=following_user
        )
        if not created:
            obj.delete()
            return Response({"follow": False})
        return Response({"follow": True})

    @action(
        methods=["get"], url_path="users/(?P<user_id>[^/.]+)/following", detail=False
    )
    def get_user_followings(self, request, user_id=None):
        user = get_object_or_404(User, id=user_id)
        followings = FollowLinks.objects.filter(follower=user)
        serializer = FollowSerializer(followings, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"], url_path="users/(?P<user_id>[^/.]+)/follower", detail=False
    )
    def get_user_followers(self, request, user_id=None):
        user = get_object_or_404(User, id=user_id)
        followers = FollowLinks.objects.filter(following=user)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)
