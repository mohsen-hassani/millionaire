from account.models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'is_staff'
        )
        labels = {
            'is_staff': 'Is Admin'
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            'surname'
        )
    def save(self, user, commit=True):
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile


class UserRegisterationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
        )