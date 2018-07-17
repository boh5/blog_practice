from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from account.forms import RegistrationForm, UserProfileForm, UserForm, UserInfoForm
# def user_login(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             cd = login_form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#
#             if user:
#                 login(request, user)
#                 return HttpResponse('Wellcome You. You have been authenticated successfully!')
#             else:
#                 return HttpResponse('Sorry. Your username or password is not right!')
#         else:
#             return HttpResponse('Invalid login!')
#
#     if request.method == 'GET':
#         login_form = LoginForm()
#         return render(request, 'account/login.html', {'login_form': login_form})
from account.models import UserProfile, UserInfo


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return redirect('account:user_login')
        else:
            return redirect('account:user_register')
    else:
        user_form = RegistrationForm()
        user_profile = UserProfileForm()
        return render(request, 'account/register.html', {'user_form': user_form, 'user_profile': user_profile})


@login_required(login_url='/account/login/')
def myself(request):
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(UserProfile, user=user)
    user_info = get_object_or_404(UserInfo, user=user)
    context = {
        'user': user,
        'user_profile': user_profile,
        'user_info': user_info,
    }

    return render(request, 'account/myself.html', context)


@login_required(login_url='/account/login/')
def myself_edit(request):
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(UserProfile, user=user)
    user_info = get_object_or_404(UserInfo, user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        user_info_form = UserInfoForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid() and user_info_form.is_valid():
            user_cd = user_form.cleaned_data
            user_profile_cd = user_profile_form.cleaned_data
            user_info_cd = user_info_form.cleaned_data

            user.email = user_cd['email']
            user_profile.birth = user_profile_cd['birth']
            user_profile.phone = user_profile_cd['phone']
            user_info.school = user_info_cd['school']
            user_info.company = user_info_cd['company']
            user_info.profession = user_info_cd['profession']
            user_info.address = user_info_cd['address']
            user_info.about_me = user_info_cd['about_me']
            user.save()
            user_profile.save()
            user_info.save()
            return redirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(initial={'birth': user_profile.birth, 'phone': user_profile.phone})
        user_info_form = UserInfoForm(initial={
            'school': user_info.school,
            'company': user_info.company,
            'profession': user_info.profession,
            'address': user_info.address,
            'about_me': user_info.about_me
        })
        return render(request, 'account/myself_edit.html', {
            'user_form': user_form,
            'user_profile_form': user_profile_form,
            'user_info_form': user_info_form
        })


@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        user_info = get_object_or_404(UserInfo, user=request.user.id)
        user_info.photo = img
        user_info.save()
        return HttpResponse('1')
    else:
        return render(request, 'account/imagecrop.html')
