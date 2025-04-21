from django.urls import path
from . import views

urlpatterns = [
    path(
        'elections/',
        views.elections,
        name='elections'
        ),
    path(
        'elections/<str:pk>/',
        views.election_detail,
        name='election_detail'
        ),
]
