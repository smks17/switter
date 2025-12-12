import os
import requests

from django.http import HttpResponse
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from posts.models import MediaPost, Post
from posts.serializer import PostSerializer
from switter.settings import FEED_SERVICE_URL
from switter.utils import user_cached


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.all()
        .select_related("author")
        .prefetch_related("media", "likes", "comments")
    )
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @user_cached(timeout=60)
    def list(self, request):
        user = request.user

        resp = requests.get(
            f"http://{FEED_SERVICE_URL}/feed/home/{user.id}",
            timeout=3,
        )
        post_ids = resp.json()["ids"]

        queryset = self.get_queryset().filter(id__in=post_ids).order_by("-created_at")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Create post
    def create(self, request):
        user = request.user
        content = request.data.get("content")
        files = request.FILES.getlist("media")

        if not content:
            return Response({"error": "Content required"}, status=400)

        with transaction.atomic():
            post = Post.objects.create(author=user, content=content)
            for f in files:
                MediaPost.objects.create(post=post, file=f)

        return Response(
            {"id": post.id, "message": "Post created successfully"},
            status=status.HTTP_201_CREATED,
        )

    # Post detail
    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="explore")
    @user_cached(timeout=60)
    def explore(self, request):
        user = request.user
        resp = requests.get(
            f"http://{FEED_SERVICE_URL}/feed/explore/{user.id}",
            timeout=3,
        )
        post_ids = resp.json()["ids"]

        queryset = self.get_queryset().filter(id__in=post_ids).order_by("-created_at")

        return Response(self.get_serializer(queryset, many=True).data)

    @action(detail=False, methods=["get"], url_path="me")
    def my_posts(self, request):
        user = request.user

        queryset = (
            Post.objects.filter(author=user)
            .annotate(
                likes_count=Count("likes"),
                comments_count=Count("comments", distinct=True),
            )
            .select_related("author")
            .prefetch_related("media")
            .order_by("-created_at")
        )

        return Response(self.get_serializer(queryset, many=True).data)


class DownloadView(APIView):
    def get(self, request, file_id):
        media_file = get_object_or_404(MediaPost, id=file_id)
        try:
            response = HttpResponse(
                media_file.file.read(), content_type="application/octet-stream"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(media_file.file.path)}"'
            )
            return response
        except IOError:
            return HttpResponse("File not found.", status=404)
