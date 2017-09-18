from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags

import markdown

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    # 文章正文
    body = models.TextField()
    category = models.ForeignKey(Category)
    # 文章标签，多对多关系
    tags = models.ManyToManyField(Tag, blank=True)
    # 文章摘要，可以为空
    excerpt = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User)
    # 文章阅读量
    views = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_time"]

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 若文章没有摘要，则先实例化一个markdown类用于渲染正文文本
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 从正文中截取前50个字符作为摘要
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的save方法保存数据到数据库
        super(Post, self).save(*args, **kwargs)
