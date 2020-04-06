from django.contrib import admin

# Register your models here.
from sonsuz.chat.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['uuid_id', 'sender', 'reciever', 'message', 'unread']


admin.site.register(Message, MessageAdmin)
