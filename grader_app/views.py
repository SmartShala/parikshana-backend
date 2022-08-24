# from django.db.models import Count, Sum, F
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from parikshana.custom_paginator import CustomPagination
from test_app.models import Test
from grader_app.models import AnswerSheet
from grader_app.serializers import AnswerSheetSerializer, AnswerSheetUploadSerializer
from grader_app.tasks import process_images
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

# Create your views here.


class uploadTestPaperView(generics.ListAPIView):
    """Upload Test Paper"""

    parser_classes = (MultiPartParser,)
    pagination_class = CustomPagination
    serializer_class = AnswerSheetSerializer

    def get_queryset(self):
        queryset = AnswerSheet.objects.filter(
            test__created_by=self.request.user,
            test=self.kwargs["test_id"],
        ).order_by("-updated_at")
        return queryset

    def get_object(self):
        try:
            return Test.objects.get(
                id=self.kwargs["test_id"], created_by=self.request.user
            )
        except Test.DoesNotExist:
            raise NotFound("Invalid Test ID")

    @swagger_auto_schema(
        operation_summary="Get all Answer Sheets",
        operation_description="""See all the `Answer Sheets` and their Following Details:  
        - `id` : ID of the Answer Sheet
        - `image` : Image Link of the answer Sheet
        - `student` : Student Id if the answer sheet is `processed`
        - `status` : Status of the answer sheet . Three states are possible
            - `queued` : The answer sheet is queued for processing
            - `processing` : The answer sheet is being processed
            - `successful` : The answer sheet is successfully processed
            - `failed` : The answer sheet has failed to be processed
        - `score` : Score of the answer sheet if the answer sheet `status` is `successful`
        - `failed` : Boolean value indicating if the answer sheet has failed to be processed.
        """,
        operation_id="View Answer Sheets",
    )
    def get(self, request, *args, **kwargs):
        # Setting it here to avoid manual-schema to get overwritten
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Upload Answer Sheet",
        operation_description="""Upload image file to start processing it:
        expects : `image` field with a valid image file
        
        ### PS : the request type is `multipart/form-data`
        
        ## ALl hail the `form-alities` of HTTP GOD
        """,
        operation_id="Upload Answer Sheet",
        request_body=AnswerSheetUploadSerializer,
    )
    def post(self, request, *args, **kwargs):
        test_obj: Test = self.get_object()
        image = request.FILES.get("image")
        if not image:
            raise NotFound("Image not provided")
        serializer = AnswerSheetUploadSerializer(
            data={"test": test_obj.id, "image": image}
        )
        if serializer.is_valid():
            inst = serializer.save()
            inst.job_id = process_images.apply_async(
                args=[
                    test_obj.id,
                    inst.id,
                ],
                soft_time_limit=100,
            )
            inst.save()
            return Response({"message": "Test Paper Uploaded Successfully"}, status=201)
        else:
            return Response(serializer.errors, status=400)
