from django.urls import path
from . import views

urlpatterns = [
    path(
        '<str:org_id>/elections/',
        views.elections,
        name='elections'
        ),
    path(
        '<str:org_id>/elections/<str:pk>/',
        views.election_detail,
        name='election_detail'
        ),
]
