from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(), {'template_name': 'users/login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("addpost/", views.addpost, name="addpost"),
    path("connect/", views.addconnection, name="addconnection"),
    path("profile/<str:pk>", views.profilepage, name="profilepage"),
    path("addtoconnection/<str:pk>",views.addtoconnection, name="addtoconnection"),
    path("removefromconnection/<str:pk>",views.removefromconnection, name="removefromconnection"),
    path("viewpost/<int:pk>", views.viewpost, name="viewpost"),
]