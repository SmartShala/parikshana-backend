from urllib import response
from django.db.models import Count, Sum, F

from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import NotFound, PermissionDenied

from parikshana.custom_paginator import CustomPagination
from parikshana.custom_perms import IsAdminUser

from school_app.models import SchoolSection
from test_app.serializers import (
    StandardSerializer,
    SubjectSerializer,
    TestSerializer,
    TestCreateSerializer,
)
from test_app.models import Test, Topic, Standard, Subject

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TestView(generics.ListCreateAPIView):
    """Create and List Tests under a teacher"""

    serializer_class = TestSerializer
    pagination_class = CustomPagination
    filter_fields = ("name", "id", "topic")

    def get_queryset(self):
        return (
            Test.objects.filter(created_by=self.request.user)
            .annotate(
                question_count=Count("questions"),
                total_score=Sum("test_mapping__marks"),
                topic_name=F("topic__name"),
                standard=F("topic__standard__name"),
                subject=F("topic__subject__name"),
                creator_name=F("created_by__name"),
            )
            .order_by("-updated_at")
        )

    @swagger_auto_schema(
        operation_summary="Create a Test",
        operation_description="""Create a Test under a teacher.""",
        operation_id="Create Test",
        request_body=TestCreateSerializer,
    )
    def post(self, request, *args, **kwargs):
        """Create a test"""
        serializer = TestCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateTestView(generics.RetrieveUpdateDestroyAPIView):
    """Update , retrieve and delete tests"""

    serializer_class = TestSerializer
    pagination_class = CustomPagination

    def get_object(self):
        try:
            return Test.objects.get(
                id=self.kwargs["test_id"], created_by=self.request.user
            )
        except Test.DoesNotExist:
            raise NotFound("Test not found")


class getTestFormData(APIView):
    @swagger_auto_schema(
        operation_summary="Get Test Form Data",
        operation_id="Get Test Form Data",
        operation_description="""Get Test Form data:
        Returns:
        ```
        {
            "standards":[
                id,name
            ],
            "subjects":[
                id,name
            ]
        }
        ```
        """,
    )
    def get(self, request, *args, **kwargs):
        data = {
            "standards": Standard.objects.all()
            .order_by("name")
            .values_list("id", "name"),
            "subjects": Subject.objects.all()
            .order_by("name")
            .values_list("id", "name"),
        }
        return Response(data, status=status.HTTP_200_OK)
