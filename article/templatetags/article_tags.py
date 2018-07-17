"""

@Author  : dilless
@Time    : 2018/7/17 21:56
@File    : article_tags.py
"""
import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from article.models import ArticlePost

register = template.Library()


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):
    return user.article.count()


@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_article_list = ArticlePost.objects.order_by('-create_time')[:n]
    return {'latest_article_list': latest_article_list}


@register.simple_tag
def most_commented_articles(n=5):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:n]


@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))  # 使用mark_safe返回"safe string"