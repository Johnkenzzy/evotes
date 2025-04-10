from django.urls import path
from . import views

urlpatterns = [
    path(
        '<uuid:org_id>/voters/',
        views.voters, name='voters'
        ),
    path(
        '<uuid:org_id>/voters/<uuid:pk>/',
        views.voter_detail,
        name='voter_detail'
        ),
    path(
        '<uuid:ballot_id>/votes/',
        views.votes,
        name='votes'
        ),
    path(
        '<uuid:ballot_id>/votes/<uuid:pk>/',
        views.vote_detail,
        name='vote_detail'
        ),
]
