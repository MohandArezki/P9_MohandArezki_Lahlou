from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegisterForm


class SignUpView(CreateView):
    """
    View for user registration.

    Uses the UserRegisterForm to handle user registration.
    Displays a form for user registration and redirects to the sign-in page upon successful registration.
    """
    form_class = UserRegisterForm
    template_name = "accounts/signup.html"

    def get_success_url(self):
        """
        Returns the URL to redirect to after successful user registration.
        """
        return reverse_lazy("signin")


class SignInView(LoginView):
    """
    View for user sign-in.

    Displays a form for user sign-in and redirects to the feeds page upon successful sign-in.
    """
    template_name = "accounts/signin.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Returns the URL to redirect to after successful user sign-in.
        """
        return reverse_lazy("feeds")


class SignOutView(LogoutView):
    """
    View for user sign-out.

    Redirects to the sign-in page upon successful user sign-out.
    """
    next_page = reverse_lazy("signin")


class PwdChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    View for changing user password.

    Uses PasswordChangeView along with SuccessMessageMixin to handle user password change.
    Displays a form for changing user password and displays a success message upon successful change.
    """
    template_name = "accounts/pwd_change.html"
    success_message = "Password changed"

    def get_success_url(self):
        """
        Returns the URL to redirect to after successful password change.
        """
        return reverse_lazy("feeds")
