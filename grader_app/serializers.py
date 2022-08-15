from rest_framework import serializers
from grader_app.models import AnswerSheet


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

    class Meta:
        model = AnswerSheet
        fields = (
            "id",
            "test",
            "image",
        )
        read_only_fields = ("id",)
