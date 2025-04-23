from django.urls import path
from . import views

urlpatterns = [
    path(
        'elections/',
        views.elections,
        name='elections'
        ),
    path(
        'get_elections/',
        views.get_elections,
        name='get_elections'
        ),
    path(
        'elections/<str:pk>/',
        views.election_detail,
        name='election_detail'
        ),
]
