import os
import requests

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.db import models, transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view


from posts.models import MediaPost, Post
from switter.settings import FEED_SERVICE_URL
from switter.utils import create_user_cache, user_cached
from users.utils import get_user_by_token


@api_view(["POST"])
def create_post_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    content = request.POST.get("content")
    files = request.FILES.getlist("media")
    if not content:
        return JsonResponse({"error": "Invalid json"}, status=400)
    with transaction.atomic():
        post = Post.objects.create(author=user, content=content)
        for file in files:
            MediaPost.objects.create(post=post, file=file)
    cache.delete(create_user_cache(user.id, "me"))
    return JsonResponse(
        {"id": post.id, "message": "Post created successfully"}, status=201
    )


@api_view(["GET"])
@user_cached(timeout=60)
def get_home_posts_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    resp = requests.get(
        f"http://{FEED_SERVICE_URL}/feed/home/{user.id}",
        timeout=3,
    )
    post_ids = resp.json()["ids"]
    posts = (
        Post.objects.filter(id__in=post_ids)
        .prefetch_related("media", "likes", "comments")
        .select_related("author")
        .order_by("-created_at")
    )
    result = []
    for p in posts:
        result.append(
            {
                "id": p.id,
                "content": p.content,
                "created_at": p.created_at,
                "author_username": p.author.username,
                "likes_count": p.likes_count,
                "comments_count": p.comments_count,
                "media": [m.url for m in p.media.all()],
            }
        )
    return JsonResponse(result, safe=False)


@api_view(["GET"])
@user_cached(timeout=60)
def get_explore_posts_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    resp = requests.get(
        f"http://{FEED_SERVICE_URL}/feed/explore/{user.id}",
        timeout=3,
    )
    post_ids = resp.json()["ids"]
    posts = (
        Post.objects.filter(id__in=post_ids)
        .prefetch_related("media", "likes", "comments")
        .select_related("author")
        .order_by("-created_at")
    )
    result = []
    for p in posts:
        result.append(
            {
                "id": p.id,
                "content": p.content,
                "created_at": p.created_at,
                "author_username": p.author.username,
                "likes_count": p.likes_count,
                "comments_count": p.comments_count,
                "media": [m.url for m in p.media.all()],
            }
        )
    return JsonResponse(result, safe=False)


@api_view(["GET"])
def get_my_posts_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    posts = (
        Post.objects.filter(author=user)
        .all()
        .annotate(
            likes_count=models.Count("likes"),
            comments_count=models.Count("comments", distinct=True),
            author_username=models.F("author__username"),
        )
        .order_by("-created_at")
        .values(
            "id",
            "content",
            "created_at",
            "likes_count",
            "comments_count",
            "author_username",
        )
    )
    cache.set(create_user_cache(user.id, "me"), list(posts), 3600)
    return JsonResponse(list(posts), safe=False)


@api_view(["GET"])
def get_post_details_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    comments = post.comments.values("user__username", "content", "created_at")
    likes = post.likes.values_list("user__username", flat=True)

    return JsonResponse(
        {
            "id": post.id,
            "author": post.author.username,
            "content": post.content,
            "likes_count": post.likes_count,
            "comments_count": post.comments_count,
            "likes": list(likes),
            "comments": list(comments),
            "created_at": post.created_at,
            "media": [m.url for m in post.media.all()],
        }
    )


@api_view(["GET"])
def download_media(request, file_id):
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
