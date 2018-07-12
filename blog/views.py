from django.shortcuts import render, get_object_or_404

from blog.models import BlogArticles


def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, 'blog/titles.html', {'blogs': blogs})


def blog_article(request, blog_id):
    article = get_object_or_404(BlogArticles, id=blog_id)
    publish_time = article.publish_time

    return render(request, 'blog/content.html', {'article': article, 'publish_time': publish_time})
