from django import forms
from mdeditor.fields import MDTextFormField

from sonsuz.blogs.models import Article, ArticleCategory


class ArticleForm(forms.ModelForm):


    # title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '文章标题'}))
    content = MDTextFormField()
    # tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '多个标签使用英文逗号(,)隔开'}))

    category = forms.ModelChoiceField(queryset=ArticleCategory.objects.all(), widget=forms.Select(attrs={'class': 'ui search dropdown'}))
    class Meta:
        model = Article
        fields = ["category", "title", "abstract", "content", "tags"]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '文章标题'}),
            'tags': forms.TextInput(attrs={'placeholder': '多个标签使用英文逗号(,)隔开'}),
            # 'category': forms.ModelChoiceField(queryset=ArticleCategory.objects.all(), to_field_name='catname')

        }




