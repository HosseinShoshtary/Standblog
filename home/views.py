from django.shortcuts import render
from blog.models import Article


def home(request):
    articles = Article.objects.filter(status=True)
    recent_articles = Article.objects.all()
    return render(request, template_name="home/index.html", context={"articles": articles})


def sidebar(request):
    date = {"name" : "hossein"}
    return render(request, template_name="includes/sidebar.html", context=date)