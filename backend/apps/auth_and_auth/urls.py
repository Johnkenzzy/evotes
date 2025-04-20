from django.urls import path
from . import views

urlpatterns = [
    path(
        'register/',
        views.register,
        name='register'
        ),
    path(
        'login/',
        views.admin_login,
        name='login'
        ),
    path(
        'logout/',
        views.logout,
        name='logout'
        ),
]
