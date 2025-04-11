from django.urls import path
from . import views

urlpatterns = [
    path(
        '<str:election_id>/ballots/',
        views.ballots,
        name='ballots'
        ),
    path(
        '<str:election_id>/ballots/<str:pk>/',
        views.ballot_detail,
        name='ballot_detail'
        ),
    path(
        '<str:ballot_id>/options/',
        views.options, name='options'
        ),
    path(
        '<str:ballot_id>/options/<str:pk>/',
        views.option_detail,
        name='option_detail'
        ),
]
