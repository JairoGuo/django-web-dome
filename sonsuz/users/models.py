from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
# from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(verbose_name="用户名称", blank=True, null=True, max_length=255)
    job = CharField(verbose_name="职业", blank=True, null=True, max_length=50, default="用户未填写职业信息")
    introduction = models.TextField(verbose_name="介绍", blank=True, null=True, default="用户未填写介绍")
    avatar = models.ImageField(verbose_name="头像", upload_to="users/avatars/", null=True, blank=True, default="")
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='住址', default='')
    birthday = models.DateField(verbose_name='生日', blank=True, null=True, default=timezone.now)
    website_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='个人网站', default='')
    weibo = models.URLField(max_length=255, null=True, blank=True, verbose_name='微博链接', default='')
    zhihu = models.URLField(max_length=255, null=True, blank=True, verbose_name='知乎链接', default='')
    github = models.URLField(max_length=255, null=True, blank=True, verbose_name='GitHub链接', default='')
    linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name='LinkedIn链接', default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.name:
            return self.name
        return self.username
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
