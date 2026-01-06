from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from interactions.models import FollowLinks, Like, Comment
from interactions.serializer import FollowSerializer, LikeSerializer, CommentSerializer
from posts.models import Post
from switter.kafka_producer import SwitterKafkaProducer
from switter.settings import USE_KAFKA
from switter.utils import user_cached


class PostInteractionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # -------- Likes --------

    @action(detail=True, methods=["post"])
    def likes(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {"detail": "Already liked"},
                status=status.HTTP_409_CONFLICT,
            )
        if USE_KAFKA:
            SwitterKafkaProducer().event_interaction(like)
        return Response(
            LikeSerializer(like).data,
            status=status.HTTP_201_CREATED,
        )

    @likes.mapping.delete
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response(status=status.HTTP_204_NO_CONTENT)
        like.delete()
        if USE_KAFKA:
            SwitterKafkaProducer().event_interaction(like)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @likes.mapping.get
    def list_likes(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        likes = Like.objects.filter(post=post).select_related("user")
        return Response(LikeSerializer(likes, many=True).data)

    # -------- Comments --------

    @action(detail=True, methods=["post", "get"])
    def comments(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "GET":
            comments = (
                Comment.objects.filter(post=post)
                .select_related("user")
                .order_by("-created_at")
            )
            return Response(CommentSerializer(comments, many=True).data)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(user=request.user, post=post)
        if USE_KAFKA:
            SwitterKafkaProducer().event_interaction(comment)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UserInteractionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    # -------- Followers --------

    @action(detail=True, methods=["post"], url_name="follow")
    def followers(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            return Response(
                {"detail": "Cannot follow yourself"},
                status=status.HTTP_409_CONFLICT,
            )
        follow, created = FollowLinks.objects.get_or_create(
            follower=request.user,
            following=user,
        )
        if not created:
            return Response(
                {"detail": "Already following"},
                status=status.HTTP_409_CONFLICT,
            )
        if USE_KAFKA:
            SwitterKafkaProducer().event_interaction(follow)
        return Response(
            FollowSerializer(follow).data,
            status=status.HTTP_201_CREATED,
        )

    @followers.mapping.delete
    def unfollow(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        follow = FollowLinks.objects.filter(
            follower=request.user,
            following=user,
        ).first()
        if not follow:
            return Response(status=status.HTTP_204_NO_CONTENT)
        follow.delete()
        if USE_KAFKA:
            SwitterKafkaProducer().event_interaction(follow)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @followers.mapping.get
    def list_followers(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        followers = FollowLinks.objects.filter(following=user)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="me/followers")
    @user_cached()
    def my_followers(self, request):
        follower = FollowLinks.objects.filter(following=request.user).select_related(
            "follower"
        )

        serializer = FollowSerializer(follower, many=True)
        return Response(serializer.data)

    # -------- Following --------

    @action(detail=True, methods=["get"], url_path="followings")
    def list_following(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        followers = FollowLinks.objects.filter(follower=user)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="me/followings")
    @user_cached()
    def my_following(self, request):
        following = FollowLinks.objects.filter(follower=request.user).select_related(
            "following"
        )

        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data)
