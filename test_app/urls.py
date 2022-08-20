from django.urls import path
from test_app.views import TestView, UpdateTestView, getTestFormData


app_name = "Test"

urlpatterns = [
    path("form-data/", getTestFormData.as_view(), name="getTestFormData"),
    path("", TestView.as_view(), name="Upload_Test"),  # GET POST
    path(
        "<int:test_id>/", UpdateTestView.as_view(), name="Update_Test"
    ),  # GET PUT PATCH DELETE
]
