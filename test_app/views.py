from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

# from django_filters import *
from parikshana.custom_errors import ExceptionMixin
from parikshana.custom_perms import IsAdminUser

# from .serializers import SchoolSerializer, TeacherSerializer
from .models import School, SchoolTeacher
from parikshana.custom_errors import (
    Http404,
    Http200,
    Http201,
    Http401,
    Http400,
    Http403,
)


# class 