from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import my_user_profile_view, login_view, signup_view, user_profile_view


urlpatterns = [
    path("login", login_view, name="login"),
    path("signup", signup_view, name="signup"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me", my_user_profile_view, name="my profile"),
    path("<int:user_id>", user_profile_view, name="my profile"),
]
