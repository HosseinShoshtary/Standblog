from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Article, Category, Comment, Message, Like
from django.core.paginator import Paginator
from .forms import ContactUsForm, MessageForm
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView, ArchiveIndexView, YearArchiveView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . mixins import LoginBlogRequiredMixin


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
        form = MessageForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance += 5
            instance.save()
    else:
        form = MessageForm()
    return render(request, template_name="blog/contact_us.html", context={"form": form})


# class ListView(View):
#     queryset = None
#     template_name = None
#
#     def get(self, request):
#         return render(request, self.template_name, context={"object_list": self.queryset})

class HomePageRedirect(RedirectView):
    # url = "/"
    pattern_name = "blog:list"


class ArticleList(TemplateView):
    pass


class UserList(ListView):
    queryset = User.objects.all()
    template_name = "blog/user_list.html"


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.likes.filter(article__slug=self.object.slug, user__id=self.request.user.id).exists():
            context["is_liked"] = True
        else:
            context["is_liked"] = False
        return context


# LoginRequiredMixin
class ArticleListView(LoginBlogRequiredMixin, ListView):
    model = Article
    context_object_name = "articles"
    paginate_by = 2


class ContactUsView(FormView):
    template_name = "blog/contact_us.html"
    form_class = MessageForm
    success_url = reverse_lazy("home_app:home")

    def form_valid(self, form):
        from_data = form.cleaned_data
        Message.objects.create(**from_data)
        return super().form_valid(form)


class MessageView(CreateView):
    model = Message
    fields = ("title", "text", "age", "date")
    success_url = reverse_lazy("home_app:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.all()
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.email = self.request.user.email
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        print(self.object)
        return super(MessageView, self).get_success_url()


class MessagesListView(ListView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = ("title", "text", "age")
    template_name_field = "_update_form"
    success_url = reverse_lazy("blog:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("blog:message_list")


class ArchiveIndexArticleView(ArchiveIndexView):
    model = Article
    date_field = "updated"


class YearArchiveArticleView(YearArchiveView):
    model = Article
    date_field = "pub_date"
    make_object_list = True
    allow_empty = True
    template_name = "blog/article_archive_year.html"


def like(request, slug, pk):
    try:
        like = Like.objects.get(article__slug=slug, user__id=request.user.id)
        like.delete()
        return JsonResponse({"response": "unliked"})
    except:
        Like.objects.create(article_id=pk, user_id=request.user.id)
        return JsonResponse({"response": "liked"})




