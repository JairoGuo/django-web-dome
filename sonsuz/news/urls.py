from django.urls import path
from django.views.generic import TemplateView

from sonsuz.news import  views

app_name = "news"
urlpatterns = [
    path("", views.NewsListView.as_view(), name='list'),
    path('post-news/', views.post_news, name='post_news'),
    path('news-manage/', views.NewsManageView.as_view(), name='news_manage'),
    path('delete/<str:pk>/', views.NewsDeleteView.as_view(), name='delete_news'),
    path('like/', views.like, name='post_like'),
    path('content/', views.contents, name='post_content'),
    path('post-reply/', views.post_reply, name='post_reply'),
    path('get-replies/', views.get_replies, name='get_replies'),

    # path('update-interactions/', views.update_interactions, name='update_interactions'),
]
