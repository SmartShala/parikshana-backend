from django.urls import path
from test_app.views import TestApp


app_name = "Test"

urlpatterns = [
    path("", TestApp.as_view(), name="test_app"),
]
