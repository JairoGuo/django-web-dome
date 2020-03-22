import uuid

from django.conf import settings
from django.db import models
from django.db.models import Count
from mdeditor.fields import MDTextField
from django.utils.translation import ugettext_lazy as _
from slugify import slugify
from taggit.managers import TaggableManager

# Create your models here.
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class ArticleCategory(models.Model):
    """文章类型"""
    catname = models.CharField(max_length=50, verbose_name='类别名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    def __str__(self):
        return self.catname

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = verbose_name


class ArticleQuerySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_published(self):
        """返回已发表的文章"""
        return self.filter(status="P").select_related('user').order_by('-created_at')

    def get_drafts(self):
        """返回草稿箱的文章"""
        return self.filter(status="D").select_related('user').order_by('-updated_at')

    def get_by_user(self, user):
        """返回所有的文章"""
        return self.filter(user=user).select_related('user').order_by('-updated_at')

    def get_counted_tags(self):
        """统计所有已发布的文章中，每一个标签的数量(大于0的)"""
        tag_dict = {}
        query = self.filter(status='P').annotate(tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Article(models.Model):
    STATUS = (("D", "Draft"), ("P", "Published"))
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='文章状态')  # 默认存入草稿箱
    category = models.ForeignKey(ArticleCategory, verbose_name="文章类别", null=True,
                                 blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="articles",
                             on_delete=models.SET_NULL, verbose_name='文章作者')
    article_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name="文章id")
    title = models.CharField(max_length=255, blank=False, null=False, unique=False, verbose_name='文章标题')

    abstract = models.TextField(null=True, blank=True, verbose_name='文章摘要', default='此文章还没有摘要')
    content = MDTextField(verbose_name="文章内容")
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='(URL)别名')
    tags = TaggableManager(through=UUIDTaggedItem, blank=True, help_text='多个标签使用英文逗号(,)隔开', verbose_name='文章标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间', db_index=True)
    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.slug:
            # 根据作者的username和标题生成文章在URL中的别名，保证了url的可读性也要保证唯一性
            # self.slug = slugify(self.title + self.user.username + "-" + uuid.uuid4().__str__()[0:8])
            self.slug = slugify(self.article_id.__str__())
        super(Article, self).save(*args, **kwargs)
