from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import Profile, Post
from .forms import PostCreateForm

# Create your views here.
@login_required
def home(request):
    form = PostCreateForm(request.POST or None)
    if request.method == "POST":
        if "post" in request.POST:
            if form.is_valid():
                scream = form.save(commit=False)
                scream.poster = request.user.profile_user
                scream.save() 
                messages.success(request, ("Your scream has been heard!"))
                return redirect("home")
        if "like" in request.POST:
            print(request.POST)

    context = { "name": request.user, "posts": Post.objects.all().order_by("-post_time"), "form": form}
    return render(request, 'twitclone/home.html', context)

@login_required
def profile(request, profile_name):
    if Profile.objects.filter(user__username=profile_name).exists():
        profile = Profile.objects.get(user__username=profile_name)
        if request.method == "POST":
            if request.POST["follow"] == "follow":
                request.user.profile_user.follows.add(profile)
        
        context = { "name": request.user, "my_posts": Post.objects.filter(poster__user__username=profile_name).order_by("-post_time"), "profile": profile }
        return render(request, 'twitclone/profile.html', context)
    else:
        raise Http404()


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials")

    return render(request, "twitclone/login.html")

def logout_view(request):
  logout(request)
  return redirect("home")

class SignUp(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  template_name = "registration/signup.html"






