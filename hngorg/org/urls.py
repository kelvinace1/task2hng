from django.urls import path 
from . import views

urlpatterns = [
    #path('api/organisations/', views.get_organisations, name="get_organisations"),
    path('api/organisations/', views.create_organisation, name="create_organisation"),
    path('api/organisations/<str:orgId>/', views.get_organisation_detail, name="get_organisations_detail"),
    path('api/organisations/<str:orgId>/users', views.add_users, name="add_users"),
]
