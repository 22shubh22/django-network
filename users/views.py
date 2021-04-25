from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import messages

from .models import Profile, Post
from .forms import SignUpForm, AddPostForm, SearchConnectionForm
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
            profile = Profile.objects.filter(user = user).first()
            profile.name = form.cleaned_data.get('name')
            profile.save()
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
    connected_users = profile.connected_users.all()
    connected_users = connected_users.exclude(user=request.user)
    print("connected_users", connected_users)
    return render(request, 'home.html', {'profile': profile, 'posts':posts, 'connected_users': connected_users})

# click on post to know more about post.
@login_required
def addpost(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
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
    
@login_required
def addconnection(request):
    if request.method == "POST":
        form = SearchConnectionForm(request.POST)
        if form.is_valid():
            print("form is valid")
            mobile_number = form.cleaned_data['mobile_number']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            profiles = Profile.objects.all()
            if mobile_number:
                profiles = profiles.filter(user__username=mobile_number)
            if name:
                profiles = profiles.filter(name=name)
            if email:
                profiles = profiles.filter(user__email=email)
            profiles = profiles.exclude(user=request.user)
            print(profiles)
            print("name is " ,form.cleaned_data['name'])
            return render(request, 'addconnection.html', {'form': form, 'search_result': profiles})
        else:
            print("Form is invalid")
            return render(request, 'addconnection.html', {'form': form})
    else:
        form = SearchConnectionForm()
        return render(request, 'addconnection.html', {'form': form})

@login_required
def profilepage(request, pk):
    profile = Profile.objects.filter(user__username=str(pk)).first()
    print(profile)
    posts = Post.objects.filter(user=profile).order_by()
    print(posts)
    connected_users = profile.connected_users.all()
    print(connected_users)
    #exclude itself from connected_users
    connected_users = connected_users.exclude(id=profile.id)
    connected_users = connected_users.exclude(user=request.user)
    print(connected_users)
    current_user = Profile.objects.filter(user=request.user).first()
    current_user_connections = current_user.connected_users.all()
    # mutual connections
    mutual_connection = connected_users & current_user_connections
    if profile in current_user_connections:
        connected = True
    else:
        connected = False
    return render(request, 'profiles.html', {'profile': profile, 'posts':posts, 'connected_users': connected_users, 'mutual_connections': mutual_connection,'connected': connected})

@login_required
def addtoconnection(request, pk):
    profile= Profile.objects.filter(user__username=str(pk)).first()
    current_user = Profile.objects.filter(user=request.user).first()
    current_user.connected_users.add(profile)
    redirect_url = '/profile/' + str(pk)
    return redirect(redirect_url)

@login_required
def removefromconnection(request, pk):
    profile= Profile.objects.filter(user__username=str(pk)).first()
    current_user = Profile.objects.filter(user=request.user).first()
    current_user.connected_users.remove(profile)
    return redirect('home')