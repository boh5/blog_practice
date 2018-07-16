from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from slugify import slugify


class ArticleColumn(models.Model):
    """
    文章栏目，不设置多级
    """
    user = models.ForeignKey(User, related_name='article_column', on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name='article', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name='article_column', on_delete=models.CASCADE)
    body = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-update_time',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id, self.slug])

    def get_url_path(self):
        return reverse('article:list_article_detail', args=[self.id, self.slug])
