from django import forms
from mdeditor.fields import MDTextFormField

from sonsuz.blogs.models import Article, ArticleCategory


class ArticleForm(forms.ModelForm):


    content = MDTextFormField()
    # category = forms.ModelChoiceField(queryset=ArticleCategory.objects.all(), widget=forms.Select(attrs={'class': 'ui search dropdown'}))
    class Meta:
        model = Article
        fields = ["title", "content", "category", "abstract", "tags", "status"]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '文章标题'}),
            'tags': forms.TextInput(attrs={'placeholder': '多个标签使用英文逗号(,)隔开'}),
            'category': forms.Select(attrs={'class': 'ui search dropdown'}),
            'abstract': forms.Textarea(attrs={'placeholder': '文章摘要'})

        }




