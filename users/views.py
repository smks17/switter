import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


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
