from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("detail/<slug:slug>", views.post_detaile, name="detail"),
    path("list", views.article_list, name="list"),
    path("category/<int:pk>", views.category_detail, name="category_detail"),
    path("search/", views.search, name="search_articles"),
    path("contact_us/", views.contact_us, name="contact_us"),
    # path("Like/<slug:slug>/<int:pk>", views.like, name="like"),
]
