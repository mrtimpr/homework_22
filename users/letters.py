from django.conf import settings
from django.core.mail import send_mail


def send_welcome_email(email: str) -> None:
    send_mail(
        subject='Добро пожаловать!',
        message='Спасибо за регистрацию в сервисе.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )