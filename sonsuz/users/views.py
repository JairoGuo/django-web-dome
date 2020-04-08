from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from sonsuz.blogs.models import Article
from sonsuz.news.models import News
from sonsuz.quora.models import Question, Answer

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView): # 用户详细视图

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/user_details.html"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name", "job", "introduction", "avatar", "address", "birthday",
              "website_url", "weibo", "zhihu", "github", "linkedin"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)

user_update_view = UserUpdateView.as_view()

class UserArticlesDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(UserArticlesDetailView, self).get_context_data()
        context["articles"] = Article.objects.get_by_user(self.get_object())
        context['active'] = 'articles'
        return context


class UserNewsDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(UserNewsDetailView, self).get_context_data()
        context["newses"] = News.objects.filter(user=self.get_object(), reply=False).order_by('-updated_at')
        context['active'] = 'news'
        return context


class UserQuestionsDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(UserQuestionsDetailView, self).get_context_data()
        context["questions"] = Question.objects.get_questions_by_user(self.get_object())
        context['active'] = 'questions'
        return context


class UserAnswersDetailView(UserDetailView):
    def get_context_data(self, **kwargs):
        context = super(UserAnswersDetailView, self).get_context_data()
        context["answers"] = Answer.objects.filter(user=self.get_object()).order_by('-updated_at')
        context['active'] = 'answers'
        return context


user_articles_detail_view = UserArticlesDetailView.as_view()
user_news_detail_view = UserNewsDetailView.as_view()
user_questions_detail_view = UserQuestionsDetailView.as_view()
user_answers_detail_view = UserAnswersDetailView.as_view()




class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False


    def get_redirect_url(self):
        # return reverse("users:detail", kwargs={"username": self.request.user.username})
        return reverse("home")


user_redirect_view = UserRedirectView.as_view()
