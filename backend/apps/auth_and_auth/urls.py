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
    path(
        'verify_voter/',
        views.verify_voter,
        name='verify_voter'
    ),
]
