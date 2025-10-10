import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication


from interactions.models import Comment, Like
from posts.models import Post


def get_user_by_token(request):
    auth = JWTAuthentication()
    try:
        user, _ = auth.authenticate(request)
        return user
    except Exception:
        return None


@api_view(["POST"])
def toggle_like_view(request, post_id):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=user, post=post)
    if created:
        return JsonResponse({"message": f"Liked post {post_id}"})
    else:
        like.delete()
        return JsonResponse({"message": f"Unliked post {post_id}"})


@api_view(["POST"])
def add_comment_view(request, post_id):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    post = get_object_or_404(Post, id=post_id)

    try:
        data = json.loads(request.body)
        content = data["content"]
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    comment = Comment.objects.create(user=user, post=post, content=content)
    return JsonResponse(
        {"message": f"Comment added to post {post_id}", "comment_id": comment.id}
    )
