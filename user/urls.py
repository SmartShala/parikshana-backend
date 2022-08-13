from django.urls import path
from .views import UserCreateView

app_name = "User"

urlpatterns = [
    path("", UserCreateView.as_view(), name="user-create"),
]
