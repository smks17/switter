from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import LoginView, MyProfileView, UserProfileView, SignUpView


urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("<int:user_id>", UserProfileView.as_view(), name="get profile"),
    path("me", MyProfileView.as_view(), name="my profile"),
]
