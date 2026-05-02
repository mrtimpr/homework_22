from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from .models import User


class StyledMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()

    def _apply_bootstrap_classes(self) -> None:
        for field in self.fields.values():
            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.PasswordInput,
                    forms.ClearableFileInput,
                ),
            ):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(StyledMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'


class EmailAuthenticationForm(StyledMixin, AuthenticationForm):
    username = forms.EmailField(label='Email')


class UserProfileForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country')