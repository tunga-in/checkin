from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout


def login_user(request: HttpRequest):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(user)
        # Redirect to homepage
        return redirect('core:home')

    else:
        # Return an invalid login message
        return render('/core/login.html', {'message': 'Username or email is incorrect'})


def logout_user(request: HttpRequest):
    logout(request)
    # Redirect to login
    return redirect('core:login_user')


def home(request: HttpRequest):
    return render('/core/home.html')