from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# 标签
from blog.utils import get_file_path


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="标签")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 文章分类
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="分类名称")
    index = models.IntegerField(verbose_name='显示顺序(从小到大)', default=999)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name
        ordering = ['index', '-id']


# 文章
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name="文章标题")
    thumbnail = models.FileField(upload_to=get_file_path)
    description = models.CharField(max_length=200, verbose_name="描述")
    content = RichTextUploadingField(blank=True, null=True, verbose_name="内容")
    click_count = models.IntegerField(verbose_name="点击次数", default=0)
    is_recommend = models.BooleanField(verbose_name="是否推荐", default=False)
    is_private = models.BooleanField(verbose_name="私密内容", default=False)
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title


class CommentManager(models.Manager):
    
    def submit_comment(self, user_id, article_id, content, supercomment_id, reply_user_id):
        comment = Comment()
        comment.content = content
        comment.user_id = user_id
        comment.article_id = article_id
        if supercomment_id:
            comment.supercomment_id = supercomment_id
        if reply_user_id:
            comment.reply_to_user_id = reply_user_id
        comment.save()
        return comment
    
# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户')
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章')
    supercomment_id = models.IntegerField(blank=True, null=True, verbose_name='父级评论id')
    reply_to_user_id = models.IntegerField(blank=True, null=True, verbose_name='回复用户id')
    objects = CommentManager()
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['date_publish']

    def __str__(self):
        return str(self.id)
