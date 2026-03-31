from django.urls import path

from . import views

urlpatterns = [
    path("", views.clients, name="clients_home"),
    path("clients_register", views.register_client, name="clients_register"),
    path("client_edit/<int:client_id>/", views.edit_client, name="client_edit"),
    path("client_delete/<int:client_id>/", views.delete_client, name="client_delete"),
]
