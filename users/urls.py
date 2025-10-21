from django.urls import path

from users.views import my_user_profile_view, login_view, signup_view, user_profile_view


urlpatterns = [
    path("login", login_view, name="login"),
    path("signup", signup_view, name="signup"),
    path("me", my_user_profile_view, name="my profile"),
    path("<int:user_id>", user_profile_view, name="my profile"),
]
