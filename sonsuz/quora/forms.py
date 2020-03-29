from django import forms
from django.forms import ModelForm

from markdownx.fields import MarkdownxFormField
from mdeditor.fields import MDTextField

from sonsuz.quora.models import Question


class QuestionForm(ModelForm):

    # content = MarkdownxFormField()
    class Meta:
        model = Question
        fields = ["title", "status", "tags", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "问题标题"}),
            "status": forms.Select(attrs={"class": "ui search dropdown"}),
            "tags": forms.TextInput(attrs={'placeholder': '多个标签使用英文逗号(,)隔开'}),
            "content": MDTextField()
        }
