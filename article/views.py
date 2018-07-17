import redis
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from article.forms import ArticleColumnForm, ArticlePostForm, CommentForm, ArticleTagForm
from article.models import ArticleColumn, ArticlePost, ArticleTag
from mysite import settings

redis_db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required(login_url='/account/login/')
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()

        return render(request, 'article/column/article_column.html', {
            'columns': columns,
            'column_form': column_form,
        })

    if request.method == 'POST':
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user=request.user, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            columns = ArticleColumn.objects.filter(user=request.user)
            column_form = ArticleColumnForm()
            return render(request, 'article/column/article_column.html', {
                'columns': columns,
                'column_form': column_form,
            })


@login_required(login_url='/account/login/')
@require_POST
def rename_article_column(request):
    column_name = request.POST['column']
    column_id = request.POST['column_id']
    line = get_object_or_404(ArticleColumn, id=column_id)
    line.column = column_name
    line.save()
    return redirect('article:article_column')


@login_required(login_url='/account/login/')
@require_POST
def del_article_column(request):
    column_id = request.POST['column_id']
    line = get_object_or_404(ArticleColumn, id=column_id)
    line.delete()
    return redirect('article:article_column')


@login_required(login_url='/account/login/')
def article_post(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tag_id_list = request.POST.getlist('article_tag')
                for tag_id in tag_id_list:
                    tag = ArticleTag.objects.get(id=tag_id)
                    new_article.article_tag.add(tag)
                return redirect('article:article_list')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        this_article_column = ''
        return render(request, 'article/column/article_post.html', {
            'article_post_form': article_post_form,
            'article_columns': article_columns,
            'this_article_column': this_article_column,
            'article_tags': article_tags
        })


@login_required(login_url='/account/login/')
def article_list(request):
    # articles = ArticlePost.objects.filter(author=request.user)
    # return render(request, 'article/column/article_list.html', {
    #     'articles': articles,
    # })
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(1)
        articles = current_page.object_list
    return render(request, 'article/column/article_list.html', {
        'articles': articles,
        'page': current_page,
    })


@login_required(login_url=reverse_lazy('account:user_login'))
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, 'article/column/article_detail.html', {
        'article': article
    })


@login_required(login_url=reverse_lazy('account:user_login'))
@require_POST
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return redirect('article:article_list')
    except:
        return HttpResponse('2')


@login_required(login_url=reverse_lazy('account:user_login'))
def edit_article(request, article_id):
    if request.method == 'GET':
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        article_tags = request.user.tag.all()
        article_tags_chose = article.article_tag.all()
        this_article_form = ArticlePostForm(initial={
            'title': article.title,
            'body': article.body,
        })
        this_article_column = article.column
        return render(request, 'article/column/article_post.html', {
            'article_post_form': this_article_form,
            'article_columns': article_columns,
            'this_article_column': this_article_column,
            'article_tags': article_tags,
            'article_tags_chose': article_tags_chose
        })
    if request.method == 'POST':
        article = get_object_or_404(ArticlePost, id=article_id)
        edit_article_form = ArticlePostForm(data=request.POST)
        if edit_article_form.is_valid():
            cd = edit_article_form.cleaned_data
            try:
                article.title = cd['title']
                article.body = cd['body']
                article.column = request.user.article_column.get(id=request.POST['column_id'])
                article.save()
                tag_id_list = request.POST.getlist('article_tag')
                tags_chose = article.article_tag.all()
                for tag in tags_chose:
                    article.article_tag.remove(tag)
                for tag_id in tag_id_list:
                    tag = ArticleTag.objects.get(id=tag_id)
                    article.article_tag.add(tag)
                return redirect('article:article_detail', article_id, article.slug)
            except:
                return HttpResponse('error')
        return HttpResponse('error2')


def list_article_titles(request):
    username = request.GET.get('username')
    user_info = None
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            user_info = user.userinfo
        except:
            user_info = None
    else:
        articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(1)
        articles = current_page.object_list
    if username:
        return render(request, 'article/list/author_article_titles.html', {
            'articles': articles,
            'page': current_page,
            'user_info': user_info,
        })
    else:
        return render(request, 'article/list/article_titles.html', {
            'articles': articles,
            'page': current_page,
        })


def list_article_detail(request, article_id, slug):
    article = get_object_or_404(ArticlePost, id=article_id, slug=slug)
    total_views = redis_db.incr('article:{}:views'.format(article_id))
    redis_db.zincrby('article_ranking', article_id, 1)

    article_ranking = redis_db.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(article_ranking_id) for article_ranking_id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

    # 推荐相似文章
    article_tags_ids = article.article_tag.values_list('id', flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('article_tag')).order_by('-same_tags', '-create_time')

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'article/list/article_detail.html', {
        'article': article,
        'total_views': total_views,
        'most_viewed': most_viewed,
        'comment_form': comment_form,
        'similar_articles': similar_articles,
    })


@csrf_exempt
@require_POST
@login_required(login_url=reverse_lazy('account:user_login'))
def like_article(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == 'like':
                article.users_like.add(request.user)
                return HttpResponse('1')
            else:
                article.users_like.remove(request.user)
                return HttpResponse('2')
        except:
            return HttpResponse('No')


@login_required(login_url=reverse_lazy('account:user_login'))
def article_tag(request):
    if request.method == 'GET':
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()

        return render(request, 'article/tag/tag_list.html', {
            'article_tags': article_tags,
            'article_tag_form': article_tag_form,
        })
    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return redirect('article:article_tag')
            except:
                return HttpResponse('the data cannot be saved.')
        else:
            return HttpResponse('sorry, the form is not valid.')


@login_required(login_url=reverse_lazy('account:user_login'))
@require_POST
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return redirect('article:article_tag')
    except:
        return HttpResponse('error')


@login_required(login_url=reverse_lazy('account:user_login'))
@require_POST
def edit_article_tag(request):
    tag_id = request.POST['tag_id']
    tag_tag = request.POST['tag_tag']
    tag = get_object_or_404(ArticleTag, id=tag_id)
    tag.tag = tag_tag
    tag.save()
    return redirect('article:article_tag')
