import http
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, request

from django.urls import reverse, reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, DetailView, UpdateView
#
# from django_comments.signals import comment_was_posted
#
from sonsuz.blogs.forms import ArticleForm
from sonsuz.blogs.models import Article, ArticleCategory

from sonsuz.utils.utils import AuthorRequiredMixin
# from mydjango.notifications.views import notification_handler
#
#
class ArticleListView(ListView):
    """已发布的文章列表"""
    model = Article
    paginate_by = 5
    context_object_name = 'article_list'
    template_name = "blogs/article_list.html"

    def get_queryset(self, **kwargs):
        return Article.objects.get_published()

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['article_categories'] = ArticleCategory.objects.all()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context


class DraftListView(ArticleListView):
    """草稿箱文章列表"""
    def get_queryset(self, **kwargs):
        return Article.objects.get_drafts()



# @method_decorator(cache_page(60*60), name='get')
class ArticleCreateView(LoginRequiredMixin, CreateView):
    """创建文章"""
    model = Article
    form_class = ArticleForm
    template_name_suffix = '_create_form'
    template_name = "blogs/article_create_form.html"


    def form_valid(self, form):

        form.instance.user = self.request.user
        form.instance.status = 'P'

        # form.instance.abstract = self.request.POST["abstract"]
        # form.instance.tags = self.request.POST["tags"]
        # form.instance.category = ArticleCategory.objects.get(pk=eval(self.request.POST["category"][0]))

        print(self.request.POST)

        return super(ArticleCreateView, self).form_valid(form)

    # success_url = reverse_lazy('blogs:list')
    def get_success_url(self):
        message = "您的文章已创建成功！"  # Django框架中的消息闪现机制
        messages.success(self.request, message)  # 消息传递给下一次请求
        return reverse_lazy('blogs:list')


class ArticleDetailView(DetailView):
    """文章详情"""
    model = Article
    template_name = 'blogs/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.select_related('user').filter(
            slug=self.kwargs['slug']
        )


class ArticleUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """用户更新文章"""
    model = Article
    form_class = ArticleForm
    template_name_suffix = '_update_form'
    template_name = "blogs/article_update_form.html"

    category = None
    tags = None
    abstract = None


    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        category = request.POST['category'].strip()
        tags = request.POST['tags'].strip()
        abstract = request.POST['abstract'].strip()


    def form_valid(self, form):
        global category
        global tags
        global abstract
        print(category, tags, abstract)

        form.instance.user = self.request.user
        return super(ArticleUpdateView,self).form_valid(form)

    # success_url = reverse_lazy('blogs:list')
    def get_success_url(self):
        message = "您的文章已更新成功！"  # Django框架中的消息闪现机制
        messages.success(self.request, message)  # 消息传递给下一次请求
        return reverse_lazy('blogs:detail', kwargs={'slug': self.get_object().slug})


# def comment_notify(**kwargs):
#     """文章有评论时通知作者"""
#     actor = kwargs['request'].user
#     action_object = kwargs['comment'].content_object

#     notification_handler(actor, action_object.user, 'C', action_object)

# # 观察者模式： 订阅[列表] + 通知（同步）
# comment_was_posted.connect(receiver=comment_notify)
