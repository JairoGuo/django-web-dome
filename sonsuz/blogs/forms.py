from django import forms
from mdeditor.fields import MDTextFormField

from sonsuz.blogs.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["category", "title", "abstract", "content", "cover", "tags", "status"]

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '文章标题', "id": "title"}))
    content = MDTextFormField()
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '多个标签使用英文逗号(,)隔开'}))



