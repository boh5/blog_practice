from django.contrib import admin

from article.models import ArticleColumn


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'create_date', 'user')
    list_filter = ('column', 'user')


admin.site.register(ArticleColumn, ArticleColumnAdmin)
