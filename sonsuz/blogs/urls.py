from django.urls import path
from django.views.generic import TemplateView

from sonsuz.news import  views

app_name = "blogs"
urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/news.html"), name="list"),
]
