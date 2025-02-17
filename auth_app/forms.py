from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from auth_app.models import *
from django import forms
from django.forms import ImageField, FileInput

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class UserAuthForm(AuthenticationForm):
    class Meta:
        model = User

class ProfileForm(forms.ModelForm):
    avatar = ImageField(widget=FileInput(attrs={'id': 'image_input'}))
    bio = forms.CharField(widget=forms.Textarea, max_length=256, required=False)
    class Meta:
        model = User
        fields = ['username', 'avatar', 'bio']