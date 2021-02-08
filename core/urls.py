from django.urls import path
from . import views


app_name = 'core'


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('users', views.users, name='users'),
    path('users/add', views.add_user, name='add_user'),
    path('entrants', views.entrants, name='entrants'),
    path('entrants/add', views.add_entrant, name='add_entrant'),
    path('entrants/<int:entrant_id>/add_entry', views.add_entry, name='add_entry'),
]