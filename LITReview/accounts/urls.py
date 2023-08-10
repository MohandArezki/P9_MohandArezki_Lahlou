from django.urls import path
from .views import SignInView, SignUpView, SignOutView, PwdChangeView

urlpatterns = [
    # URL pattern for user registration.
    path("signup", SignUpView.as_view(), name="signup"),

    # URL pattern for user sign-in.
    path("signin", SignInView.as_view(), name="signin"),

    # URL pattern for user sign-out.
    path("signout", SignOutView.as_view(), name="signout"),

    # URL pattern for changing user password.
    path("pwd-change", PwdChangeView.as_view(), name="pwd_change"),
]
