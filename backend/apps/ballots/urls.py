from django.urls import path
from . import views

urlpatterns = [
    path(
        '<str:election_id>/ballots/',
        views.ballots,
        name='ballots'
        ),
    path(
        '<str:election_id>/get_ballots/',
        views.get_ballots,
        name='get_ballots'
        ),
    path(
        '<str:election_id>/ballots/<str:pk>/',
        views.ballot_detail,
        name='ballot_detail'
        ),
    path(
        '<str:ballot_id>/options/',
        views.options,
        name='options'
        ),
    path(
        '<str:ballot_id>/get_options/',
        views.get_options,
        name='get_options'
        ),
    path(
        '<str:ballot_id>/options/<str:pk>/',
        views.option_detail,
        name='option_detail'
        ),
]
