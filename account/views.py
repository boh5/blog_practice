from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from account.forms import LoginForm, RegistrationForm, UserProfileForm


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                return HttpResponse('Wellcome You. You have been authenticated successfully!')
            else:
                return HttpResponse('Sorry. Your username or password is not right!')
        else:
            return HttpResponse('Invalid login!')

    if request.method == 'GET':
        return render(request, 'account/login.html')


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
            return HttpResponse('注册成功！')
        else:
            return HttpResponse('注册失败！')
    else:
        return render(request, 'account/register.html')
