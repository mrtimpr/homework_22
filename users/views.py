from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import EmailAuthenticationForm, CustomUserCreationForm, UserProfileForm
from .letters import send_welcome_email
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        send_welcome_email(email=self.object.email)
        return response


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = EmailAuthenticationForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user