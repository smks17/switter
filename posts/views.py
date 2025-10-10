import json

from django.http import JsonResponse
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import Post


# TODO: move to another place
def get_user_by_token(request):
    auth = JWTAuthentication()
    try:
        user, _ = auth.authenticate(request)
        return user
    except Exception:
        return None


@api_view(["POST"])
def create_post_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        data = json.loads(request.body)
        content = data.get("content")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid json"}, status=400)
    post = Post.objects.create(author=user, content=content)
    return JsonResponse(
        {"id": post.id, "message": "Post created successfully"}, status=201
    )


@api_view(["GET"])
def get_all_posts_view(request):
    posts = (
        Post.objects.all()
        .order_by("-created_at")
        .values(
            "id",
            "content",
            "created_at",
            # "likes_count",
            # "comments_count",
            author_username=models.F("author__username"),
        )
    )
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
        }
    )
