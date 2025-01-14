from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    age = forms.IntegerField(required=True, min_value=1, label="Age")
    bio = forms.CharField(required=True, widget=forms.Textarea, label="Bio")
    image = forms.ImageField(required=True, label="Profile Image")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'age', 'bio','image']