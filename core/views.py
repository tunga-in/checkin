from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_user(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to homepage
            return redirect('core:home')

        else:
            # Return an invalid login message
            return render(request, 'login.html', {'message': 'Username or email is incorrect', 'username': username})

    else:
        return render(request, 'login.html')


def logout_user(request: HttpRequest):
    logout(request)
    # Redirect to login
    return redirect('core:login')


@login_required(login_url='/login')
def home(request: HttpRequest):
    return render(request, 'home.html')
