from django.shortcuts import render, get_object_or_404
from .models import Article


def post_detaile(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, template_name="blog/article_details.html", context={"article": article})


def article_list(request):
    articles = Article.objects.all()
    return render(request, template_name="blog/article.html", context={"articles": articles})
