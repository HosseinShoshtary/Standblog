from django.shortcuts import render
from blog.models import Article


def home(request):
    articles = Article.objects.all()
    return render(request, template_name="home/index.html", context={"articles": articles})
