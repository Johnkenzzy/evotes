from django.urls import path
from . import views

urlpatterns = [
    path(
        'organizations/',
        views.organizations,
        name='organizations'
        ),
    path(
        'organizations/<str:pk>/',
        views.organization_detail,
        name='organization_detail'
        ),
    path(
        '<str:org_id>/admins/',
        views.admins, name='admins'
        ),
    path(
        '<str:org_id>/admins/<str:pk>/',
        views.admin_detail,
        name='admin_detail'
        ),
]
