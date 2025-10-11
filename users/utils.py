from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_by_token(request):
    auth = JWTAuthentication()
    try:
        user, _ = auth.authenticate(request)
        return user
    except Exception:
        return None
