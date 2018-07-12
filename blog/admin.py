from django.contrib import admin

from blog.models import BlogArticles


class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_time')
    list_filter = ('publish_time', 'author')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish_time'
    ordering = ['publish_time', 'author']


admin.site.register(BlogArticles, BlogArticleAdmin)
