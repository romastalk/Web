"""
Definition of views.
"""

from datetime import datetime

from django.http import HttpRequest


import imp
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from app.forms import AnketaForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import BlogForm, CommentForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Контактная страница.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О компании',
            'message':'Компания была основанна в 1990 году.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Ссылки.',
            'year':datetime.now().year,
        }
    )

def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    reviews_choice = {"1": "Нормально", "2": "Хорошо", "3": "Отлично"}
    list_reviews_choice = {"1": "Ничего", "2": "Совсем ничего", "3": "Всё хорошо"}
    if request.method == "POST":
        form = AnketaForm(request.POST)
        if form.is_valid():
            average_rating = 0
            data = dict()

            data["name"] = form.cleaned_data["name"]

            rating = form.cleaned_data["design"]
            average_rating += int(rating)
            data["design"] = reviews_choice[rating]

            rating = form.cleaned_data["color_palette"]
            average_rating += int(rating)
            data["color_palette"] = reviews_choice[rating]

            rating = form.cleaned_data["icon"]
            average_rating += int(rating)
            data["icon"] = reviews_choice[rating]

            data["what_change"] = list_reviews_choice[form.cleaned_data["what_change"]]

            data["impressions"] = form.cleaned_data["impressions"]
            data["average_rating"] = reviews_choice[str(round(average_rating / 3))]

            if form.cleaned_data["visit"]:
                data["visit"] = "Да"
            else:
                data["visit"] = "Нет"

            form = None
    else:
        form = AnketaForm()
    return render(request, "app/pool.html", {"form": form, "data": data})



def registration(request):
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()

            return redirect("home")

    else:
        regform = UserCreationForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/registration.html",
        {
            "regform": regform,
            "year": datetime.now().year,
        },
    )


def blog(request):
    posts = Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/blog.html",
        {
            "title": "Блог",
            "posts": posts,
            "year": datetime.now().year,
        },
    )

def blogpost(request, parametr):
    post = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()

            return redirect("blogpost", parametr=post.id)
    else:
        form = CommentForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/blogpost.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "year": datetime.now().year,
        },
    )

def newpost(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        "app/newpost.html",
        {
            "blogform": blogform,
            "title": "Добавить статью блога",
            "year": datetime.now().year,
        },
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/videopost.html",
        {
            "title": "Видео",
            "year": datetime.now().year,
        },
    )






