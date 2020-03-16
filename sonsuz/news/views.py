from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from sonsuz.news.models import News
from sonsuz.utils.utils import ajax_required, AuthorRequiredMixin



class NewsListView(ListView):
    model = News
    paginate_by = 10
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'


class NewsManageView(ListView):
    model = News
    paginate_by = 10
    template_name = 'news/news_manages.html'
    # context_object_name = 'news_list'

@login_required
@ajax_required
@require_http_methods(["POST"])
def post_news(request):
    """发送动态，AJAX POST请求"""
    newsContent = request.POST['news_content'].strip()
    newsTitle = request.POST['news_title'].strip()
    if newsContent:
        news = News.objects.create(user=request.user, content=newsContent, title=newsTitle)
        html = render_to_string('news/news_single.html', {'news': news, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空！")

# class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView)
class NewsDeleteView(LoginRequiredMixin, DeleteView):
# class NewsDeleteView(DeleteView):

    """删除一条新闻记录"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:news_manage') # 在项目的URLConf未加载前使用


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    """点赞，响应AJAX POST请求"""
    news_id = request.POST['newsId']
    news = News.objects.get(pk=news_id)
    # 取消或者添加赞
    news.switch_like(request.user)
    # 返回赞的数量
    return JsonResponse({"likers_count": news.likers_count()})



# @login_required
@ajax_required
@require_http_methods(["POST"])
def contents(request):

    news_id = request.POST['newsId']
    news = News.objects.get(pk=news_id)
    like_flag = "outline"
    if request.user in news.get_likers():
        like_flag = "inline"

    return JsonResponse({"news_conent": news.get_content(),
                         "news_title": news.title,
                         "news_like_count": news.likers_count(),
                         "news_like_flag": like_flag
                         })



@login_required
@ajax_required
@require_http_methods(["POST"])
def post_reply(request):
    """发送回复，AJAX POST请求"""
    replyContent = request.POST['reply-content']
    parentId = request.POST['newsId']
    parent = News.objects.get(pk=parentId)
    if replyContent:
        parent.reply_this(request.user, replyContent)
        return JsonResponse({'newsid': parent.pk,'replies_count': parent.replies_count()})
    else:
        return HttpResponseBadRequest("内容不能为空！")
#
#
# @ajax_required
# @require_http_methods(["GET"])
# def get_replies(request):
#     """返回新闻的评论，AJAX GET请求"""
#     news_id = request.GET['newsId']
#     news = News.objects.get(pk=news_id)
#     # render_to_string()表示加载模板，填充数据，返回字符串
#     replies_html = render_to_string("news/reply_list.html", {"replies": news.get_children()})  # 有评论的时候
#     return JsonResponse({
#         "newsid": news_id,
#         "replies_html": replies_html,
#     })
#
#
# @login_required
# def update_interactions(request):
#     """更新互动信息"""
#     data_point = request.GET['id_value']
#     news = News.objects.get(pk=data_point)
#     return JsonResponse({'likes': news.likers_count(), 'replies': news.replies_count()})
