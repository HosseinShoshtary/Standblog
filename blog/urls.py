from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("detail/<slug:slug>", views.post_detaile, name="detail"),
    path("list", views.ArticleListView.as_view(), name="list"),
    path("category/<int:pk>", views.category_detail, name="category_detail"),
    path("search/", views.search, name="search_articles"),
    path("contact_us/", views.MessageView.as_view(), name="contact_us"),
    path("users", views.UserList.as_view(), name="user_list"),
    path("red", views.HomePageRedirect.as_view(), name="redirect"),
    # path("Like/<slug:slug>/<int:pk>", views.like, name="like"),
]
