from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import messages

from .models import Profile, Post
from .forms import SignUpForm, AddPostForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

@login_required
def home(request):
    profile = Profile.objects.filter(user=request.user).first()
    print(request.user)
    print(profile)
    posts = Post.objects.filter(user=profile).order_by()
    print(posts)
    return render(request, 'home.html', {'profile': profile, 'posts':posts})

@login_required
def addpost(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # TODO: form image field is not working properly
            profile = Profile.objects.filter(user=request.user).first()
            print(profile)
            post.user = profile
            post.save()
            return redirect('home')
        else:
            print("Form was not valid")
            return render(request, 'addpost.html', {'form': form})
    else:
        form = AddPostForm()
        return render(request, 'addpost.html', {'form': form})
    