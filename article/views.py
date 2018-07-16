from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST

from article.forms import ArticleColumnForm, ArticlePostForm
from article.models import ArticleColumn, ArticlePost


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
                return redirect('article:article_list')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        this_article_column = ''
        return  render(request, 'article/column/article_post.html', {
            'article_post_form': article_post_form,
            'article_columns': article_columns,
            'this_article_column': this_article_column
        })


@login_required(login_url='/account/login/')
def article_list(request):
    # articles = ArticlePost.objects.filter(author=request.user)
    # return render(request, 'article/column/article_list.html', {
    #     'articles': articles,
    # })
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 2)
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
        this_article_form = ArticlePostForm(initial={
            'title': article.title,
            'body': article.body,
        })
        this_article_column = article.column
        return render(request, 'article/column/article_post.html', {
            'article_post_form': this_article_form,
            'article_columns': article_columns,
            'this_article_column': this_article_column
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
                return redirect('article:article_detail', article_id, article.slug)
            except:
                return HttpResponse('error')
        return HttpResponse('error2')


def list_article_titles(request):
    articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title, 2)
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
    return render(request, 'article/list/article_titles.html', {
        'articles': articles,
        'page': current_page
    })


def list_article_detail(request, article_id, slug):
    article = get_object_or_404(ArticlePost, id=article_id, slug=slug)
    return render(request, 'article/list/article_detail.html', {'article': article})

