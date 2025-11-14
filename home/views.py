from django.shortcuts import render
from blog.models import Article


def home(request):
    articles = Article.objects.filter(status=True)
    recent_articles = Article.objects.all()[:3]
    return render(request, template_name="home/index.html", context={"articles": articles, "recent_articles": recent_articles})
