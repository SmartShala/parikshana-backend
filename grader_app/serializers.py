from rest_framework import serializers
from grader_app.models import AnswerSheet, AnsweredQuestion
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

    class Meta:
        model = AnswerSheet
        fields = (
            "id",
            "test",
            "image",
        )
        read_only_fields = ("id",)


class AnsweredQuestionSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source="question.question")
    answer = serializers.SerializerMethodField()
    correct_answer = serializers.SerializerMethodField()
    options = serializers.ListField(child=serializers.CharField())
    correct_answer = serializers.SerializerMethodField()

    class Meta:
        model = AnsweredQuestion
        fields = (
            "answer",
            "question",
            "is_correct",
            "options",
            "correct_answer",
        )

    def get_answer(self, obj):
        return obj.question.options[obj.answer]

    def get_correct_answer(self, obj):
        return obj.question.options[obj.question.correct_option]
