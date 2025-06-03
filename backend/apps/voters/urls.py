from django.urls import path
from . import views

urlpatterns = [
    path(
        'voters/',
        views.voters,
        name='voters'
        ),
    path(
        'voters/send_codes/',
        views.send_codes,
        name='send_codes'
        ),
    path(
        'voters/<str:pk>/',
        views.voter_detail,
        name='voter_detail'
        ),
    path(
        'voter/<str:pk>/',
        views.get_voter,
        name='get_voter'
        ),
    path(
        '<str:ballot_id>/cast_votes/',
        views.cast_votes,
        name='cast_votes'
        ),
    path(
        '<str:ballot_id>/get_votes/',
        views.get_votes,
        name='get_votes'
        ),
    path(
        '<str:ballot_id>/votes/',
        views.vote_detail,
        name='vote_detail'
        ),
]
