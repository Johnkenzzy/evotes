from django.urls import path
from . import views

urlpatterns = [
    path(
        '<uuid:election_id>/elections/',
        views.ballots, name='ballots'
        ),
    path(
        '<uuid:election_id>/elections/<uuid:pk>/',
        views.ballot_detail,
        name='ballot_detail'
        ),
    path(
        '<uuid:ballot_id>/ballots/',
        views.options, name='options'
        ),
    path(
        '<uuid:ballot_id>/ballots/<uuid:pk>/',
        views.option_detail,
        name='option_detail'
        ),
]
