from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import messages

from .models import Profile
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})