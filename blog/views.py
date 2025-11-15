from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator


def post_detaile(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, template_name="blog/article_details.html", context={"article": article})


def article_list(request):
    articles = Article.objects.all()
    page_number = request.GET.get("page")
    print(page_number)
    paginator = Paginator(articles, 2)
    object_list = paginator.get_page(page_number)
    return render(request, template_name="blog/article_list.html", context={"articles": object_list})


def category_detail(request, pk):
    category = get_object_or_404(Category, id=pk)
    articles = category.articles.all()
    return render(request, template_name="blog/article_list.html", context={"articles": articles})