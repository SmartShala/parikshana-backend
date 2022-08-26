from django.urls import path
from student_app.views import StudentDetailView


app_name = "Student"

urlpatterns = [
    path("login/<str:std_id>/", StudentDetailView.as_view(), name="student_login"),
]
