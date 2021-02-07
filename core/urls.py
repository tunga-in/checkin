from django.urls import path
from . import views


app_name = 'core'


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('users', views.users, name='users')
]