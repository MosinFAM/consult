from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="Имя")
    last_name = forms.CharField(max_length=30, required=False, label="Фамилия")

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Объединенная форма
class UserProfileUpdateForm(forms.Form):
    user_form = UserUpdateForm()
    profile_form = ProfileUpdateForm()

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.user_form = UserUpdateForm(instance=user)
            self.profile_form = ProfileUpdateForm(instance=user.profile)