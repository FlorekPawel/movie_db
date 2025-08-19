from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="", max_length=20, required=True, widget=forms.TextInput(attrs={
                "placeholder": "Username"
            })
    )
    email = forms.EmailField(label="",required=True, widget=forms.TextInput(attrs={
                "placeholder": "Email"
            }))
    
    password1 = forms.CharField(
        label="",
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "password-field",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="",
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat password",
                "class": "password-field",
                "autocomplete": "new-password",
            }
        ),
    )
    usable_password = None

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
