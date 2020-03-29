from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from sonsuz.chat import views

app_name = "chat"
urlpatterns = [
    path('', views.MessagesListView.as_view(), name='messages_list'),
    path('send-message/', views.send_message, name='send_message'),
    path('<str:username>/', views.ConversationListView.as_view(), name='conversation_detail'),


]
