import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from users.utils import get_user_by_token


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid json"}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "User login successfully",
                "username": user.username,
                "user_id": user.id,
            },
            status=200,
        )
    else:
        return JsonResponse(
            {"error": "Invalid credential"},
            status=401,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid json"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "User is already exists"}, status=400)
    else:
        user = User(username=username)
        user.set_password(password)
        user.save()
        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "User created successfully",
            },
            status=200,
        )


@api_view(["GET"])
def my_user_profile_view(request):
    user = get_user_by_token(request)
    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)
    return get_user_profile(user)


@api_view(["GET"])
def user_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return get_user_profile(user)


def get_user_profile(user: User):
    return JsonResponse(
        {
            "username": user.username,
            "number_following": user.list_followings.count(),
            "number_follower": user.list_followers.count(),
            # TODO: add more
        }
    )
