from .form import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render


def my_home(request):
    return render(request, 'index.html')


def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                messages.success(request, 'login success.')
                return render(request, 'index.html', locals())
        messages.success(request, 'username or password error.')
        return render(request, 'login_page.html', locals())
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login_page.html', locals())


def my_logout(request):
    logout(request)
    messages.success(request, 'logout success.')
    return render(request, 'index.html', locals())
