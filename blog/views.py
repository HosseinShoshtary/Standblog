from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Comment, Like
from django.core.paginator import Paginator
from . forms import ContactUsForm


def post_detaile(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        parent_id = request.POST.get("parent_id")
        body = request.POST.get("body")
        Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)
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


def search(request):
    q = request.GET.get("q")
    articles = Article.objects.filter(title__contains=q)
    page_number = request.GET.get("page")
    print(page_number)
    paginator = Paginator(articles, 2)
    object_list = paginator.get_page(page_number)
    return render(request, template_name="blog/article_list.html", context={"articles": object_list})


def contact_us(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["text"])
            return redirect("home_app:home")
    form = ContactUsForm()
    return render(request, template_name="blog/contact_us.html", context={"form": form})


def like(request, slug, pk):
    try:
        like = Like.objects.get(article__slug=slug, user__id=request.user.id)
        like.delete()
    except:
        Like.objects.create(article_id=pk, user_id=request.user.id)

    return redirect("blog:detail", slug)
