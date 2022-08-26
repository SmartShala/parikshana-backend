from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from parikshana.custom_paginator import CustomPagination
from test_app.models import Test
from student_app.serializers import StudentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import (
    ParseError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
    NotAcceptable,
    UnsupportedMediaType,
    Throttled,
)
from school_app.models import SchoolStudent


class StudentDetailView(generics.RetrieveAPIView):
    serializer_class = StudentSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        print(self.kwargs["std_id"])
        obj = SchoolStudent.objects.filter(std_id=self.kwargs["std_id"])
        if not obj.exists():
            raise NotFound("Invalid Student ID")
        return obj.first()
