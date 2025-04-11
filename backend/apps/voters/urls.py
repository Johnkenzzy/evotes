from django.urls import path
from . import views

urlpatterns = [
    path(
        '<str:org_id>/voters/',
        views.voters,
        name='voters'
        ),
    path(
        '<str:org_id>/voters/<str:pk>/',
        views.voter_detail,
        name='voter_detail'
        ),
    path(
        '<str:ballot_id>/votes/',
        views.votes,
        name='votes'
        ),
    path(
        '<str:ballot_id>/votes/<str:pk>/',
        views.vote_detail,
        name='vote_detail'
        ),
]
