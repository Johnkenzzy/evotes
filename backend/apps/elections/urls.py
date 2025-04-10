from django.urls import path
from . import views

urlpatterns = [
    path(
        '<uuid:org_id>/elections/',
        views.elections, name='elections'
        ),
    path(
        '<uuid:org_id>/elections/<uuid:pk>/',
        views.election_detail,
        name='admin_detail'
        ),
]
