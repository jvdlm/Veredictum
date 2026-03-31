from django.urls import path

from . import views

urlpatterns = [
    path("", views.process, name="processes"),
    path("process_register", views.register_process, name="process_register"),
    path("process_edit/<int:process_id>/", views.edit_process, name="process_edit"),
    path("process_delete/<int:process_id>/", views.delete_process, name="process_delete"),
    path("relatorios/", views.process_reports, name="process_reports"),
]
