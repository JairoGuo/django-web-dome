from django.urls import path
from django.views.generic import TemplateView

from sonsuz.blogs import  views

app_name = "blogs"
urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("article-create", views.ArticleCreateView.as_view(), name="create"),
]
