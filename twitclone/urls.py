from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("account/", include("django.contrib.auth.urls"), name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/<str:profile_name>', views.profile, name='profile'),
]