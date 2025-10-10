import json

from django.http import JsonResponse
from django.db import models
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import Post


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
        .values("id", "content", "created_at", author=models.F("author__username"))
    )
    return JsonResponse(list(posts), safe=False)
