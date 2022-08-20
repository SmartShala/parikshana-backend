from rest_framework import serializers
from grader_app.models import AnswerSheet
from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method


class AnswerSheetSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnswerSheet
        fields = (
            "id",
            "image",
            "test",
            "student",
            "status",
            "created_at",
            "updated_at",
            "failed",
            "score",
        )
        read_only_fields = ("id",)

    def get_student(self, obj):
        if obj.student:
            return obj.student.name
        return None


class AnswerSheetUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    test = serializers.IntegerField(required=False)

    class Meta:
        model = AnswerSheet
        fields = (
            "id",
            "test",
            "image",
        )
        read_only_fields = ("id",)
