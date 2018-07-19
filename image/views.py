from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from image.forms import ImageForm
from image.models import Image


@login_required(login_url=reverse_lazy('account:user_login'))
@require_POST
def upload_image(request):
    form = ImageForm(request.POST)
    if form.is_valid():
        try:
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return JsonResponse({'status': '1'})
        except:
            return JsonResponse({'status': '0'})


@login_required(login_url=reverse_lazy('account:user_login'))
def list_images(request):
    images = Image.objects.filter(user=request.user)
    paginator = Paginator(images, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        images = current_page.object_list
    except PageNotAnInteger or EmptyPage:
        current_page = paginator.page(1)
        images = current_page.object_list
    return render(request, 'image/list_images.html', {
        'images': images,
        'page': current_page
    })


@login_required(login_url=reverse_lazy('account:user_login'))
@require_POST
def del_image(request):
    image_id = request.POST['image_id']
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('image:list_images')


def falls_images(request):
    images = Image.objects.all()
    return render(request, 'image/falls_images.html', {
        'images': images,
    })
