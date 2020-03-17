from django.contrib import admin
from django.db import models

from sonsuz.blogs.models import Article, ArticleCategory

from mdeditor.widgets import MDEditorWidget


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['catname', 'created_at', 'updated_at']


class ArticleAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.TextField: {'widget': MDEditorWidget}
    # }
    list_display = ['slug', 'title', 'user', 'category', 'status', 'tags', 'created_at']


admin.site.register(ArticleCategory, ArticleCategoryAdmin)

admin.site.register(Article, ArticleAdmin)
