from django.db.models import Count, Sum, F
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from parikshana.custom_paginator import CustomPagination
from parikshana.custom_perms import IsAdminUser

from parikshana.custom_errors import (
    Http404,
    Http200,
    Http201,
    Http401,
    Http400,
    Http403,
)
from test_app.serializers import TestSerializer
from test_app.models import Test


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
            raise Http404("Test not found")
