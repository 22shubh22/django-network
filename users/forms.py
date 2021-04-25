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
    # TODO: remove self form allowed profiles
    allowed_profiles = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Post
        fields = ("title", "text", "image","allowed_profiles")
    
class SearchConnectionForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    email = forms.CharField(max_length=200, required=False)
    mobile_number = forms.CharField(max_length=200, required=False)

