from core.models import Entrant, Temperature
from django.contrib.auth.models import User
from core.helpers import UserHelper
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
    return render(request, 'home.html', {'data': Temperature.objects.all().order_by('-timestamp')})


@login_required(login_url='/login')
def entrants(request: HttpRequest):
    return render(request, 'entrants/list.html', {'entrants': Entrant.objects.all()})


@login_required(login_url='/login')
def users(request: HttpRequest):
    return render(request, 'users/list.html', {'users': User.objects.all()})


@login_required(login_url='/login')
def add_user(request: HttpRequest):
    context = {}
    context['text_button'] = 'Submit'
    context['text_title'] = 'Add User'

    if request.method == 'POST':
        # Persist user data to database
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        user_helper = UserHelper(
            first_name=first_name, last_name=last_name, username=username, password=password)
        is_valid, errors = user_helper.validate()
        if is_valid:
            user_helper.save()
            return redirect('core:users')

        else:
            context['errors'] = errors
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['username'] = username
            context['password'] = password
            return render(request, 'users/form.html', context)

    else:
        # Return add user form
        return render(request, 'users/form.html', context)


@login_required(login_url='/login')
def add_entrant(request: HttpRequest):
    context = {}
    context['text_button'] = 'Submit'
    context['text_title'] = 'Add Entrant'

    if request.method == 'POST':
        # Persist user data to database
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        tel_number = data.get('tel_number')
        id_number = data.get('id_number')
        company = data.get('company')
        reading = data.get('reading')
        timestamp = data.get('date')

        entrant = Entrant(first_name=first_name, last_name=last_name,
                          company=company, tel_number=tel_number, id_number=id_number)
        is_valid, errors = entrant.validate()
        if is_valid:
            entrant.create_entry(reading, timestamp)
            return redirect('core:home')

        else:
            context['errors'] = errors
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['company'] = company
            context['tel_number'] = tel_number
            context['id_number'] = id_number
            context['reading'] = reading
            context['date'] = timestamp
            return render(request, 'entrants/form.html', context)

    else:
        # Return add user form
        return render(request, 'entrants/form.html', context)


@login_required(login_url='/login')
def add_entry(request: HttpRequest, entrant_id: int):
    context = {}
    context['text_button'] = 'Submit'
    context['text_title'] = 'Add Entrant'

    entrant = Entrant.objects.get(id=entrant_id)

    context['first_name'] = entrant.first_name
    context['last_name'] = entrant.last_name
    context['tel_number'] = entrant.tel_number
    context['id_number'] = entrant.id_number
    context['company'] = entrant.company

    if request.method == 'POST':
        # Persist user data to database
        data = request.POST
        reading = data.get('reading')
        timestamp = data.get('date')

        temp = Temperature(reading=reading, timestamp=timestamp, user=entrant)
        temp.save()
        return redirect('core:home')

    else:
        # Return add user form
        return render(request, 'entrants/form.html', context)