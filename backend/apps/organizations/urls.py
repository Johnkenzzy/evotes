from django.urls import path
from . import views

urlpatterns = [
    path(
        'organizations/',
        views.organizations,
        name='organizations'
        ),
    path(
        'organizations/<uuid:pk>/',
        views.organization_detail,
        name='organization_detail'
        ),
    path(
        '<uuid:org_id>/admins/',
        views.admins, name='admins'
        ),
    path(
        '<uuid:org_id>/admins/<uuid:pk>/',
        views.admin_detail,
        name='admin_detail'
        ),
]
