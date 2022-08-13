from django.urls import path
from .views import (
    CreateSchool,
    UpdateDeleteSchool,
    AddGetTeachers,
    UpdateDeleteTeachers,
)

app_name = "School"

urlpatterns = [
    path("", CreateSchool.as_view(), name="Create-Get-School"),  # GET POST
    path(
        "<int:school_id>/", UpdateDeleteSchool.as_view(), name="Update-Delete-School"
    ),  # GET POST PUT PATCH DELETE
    path(
        "<int:school_id>/teachers/", AddGetTeachers.as_view(), name="Add-Get-Teachers"
    ),  # GET POST
    path(
        "<int:school_id>/teachers/<int:teacher_id>/",
        UpdateDeleteTeachers.as_view(),
        name="Update-Delete-Teachers",
    ),  # GET PATCH PUT DELETE
]
