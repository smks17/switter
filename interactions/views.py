import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view


from interactions.models import Comment, FollowLinks, Like
from posts.models import Post
from users.utils import get_user_by_token


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


@api_view(["GET"])
def my_comments_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    comments = Comment.objects.filter(user=user).values("post", "content").all()
    return JsonResponse(list(comments), safe=False)


@api_view(["GET"])
def my_likes_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    posts = Like.objects.filter(user=user).values("post").all()
    return JsonResponse(list(posts), safe=False)


@api_view(["POST", "DELETE"])
def follow_view(request, user_id):
    curr_user = get_user_by_token(request)
    if not curr_user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    user = get_object_or_404(User, id=user_id)
    assert user.id != curr_user.id
    if request.method == "POST":
        FollowLinks.objects.create(
            follower=curr_user,
            following=user,
        )
        return JsonResponse({"message": f"You started following {user.id}"})
    elif request.method == "DELETE":
        follow_link = FollowLinks.objects.filter(
            follower=curr_user,
            following=user,
        ).get()
        follow_link.delete()
        return JsonResponse({"message": f"You unfollow {user.id}"})


@api_view(["GET"])
def my_followers_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    followers = FollowLinks.objects.filter(following=user).values("following_id").all()
    return JsonResponse(list(followers), safe=False)


@api_view(["GET"])
def my_followings_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    followings = FollowLinks.objects.filter(follower=user).values("follower_id").all()
    return JsonResponse(list(followings), safe=False)
