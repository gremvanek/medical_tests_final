# user.forms
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import BooleanField

from .models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "phone",
            "avatar",
            "country",
            "is_verified",
            "have_permissions",
        ]


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email не найден.")
        return email


class VerificationCodeResetForm(forms.Form):
    email = forms.EmailField(label="Email")


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'autofocus': True})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
