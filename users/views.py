from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EmailAuthenticationForm, CustomUserCreationForm, UserProfileForm
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            send_mail(
                subject='Добро пожаловать!',
                message='Спасибо за регистрацию в сервисе.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.object.email],
                fail_silently=False,
            )
        except Exception:
            pass
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