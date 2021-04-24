from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=False, help_text='Optional. name')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password1', 'password2',)

class AddPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=100, required=True, help_text='Input post title')
    # post = forms.CharField(max_length=500, required=False)
    # image = forms.ImageField()
    #class meta maybe not necessary

    class Meta:
        model = Post
        fields = ("title", "text", "image",)