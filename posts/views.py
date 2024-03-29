from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    latest = Post.objects.all()[:11]
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def new_post(request):
    if request.method != "POST":
        form = PostForm(request.POST)
        return render(request, "new.html", {"form": form})
    form = PostForm(request.POST)
    if not form.is_valid():
        return render(request, "new.html", {"form": form})
    post = form.save(commit=False)
    username = request.user.username
    post.author = User.objects.get(username=username)
    post.save()
    return redirect("index")
