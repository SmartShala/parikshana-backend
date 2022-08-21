from rest_framework import serializers
from test_app.models import Question, Standard, Subject, Test, Topic
from drf_yasg.utils import swagger_serializer_method


class TestCreateSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(write_only=True)
    standard = serializers.IntegerField(write_only=True)
    subject = serializers.IntegerField(write_only=True)
    creator_name = serializers.CharField(read_only=True)

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "description",
            "topic",
            "standard",
            "subject",
            "creator_name",
            "updated_at",
        )

    def create(self, validated_data):
        "Overloading to add created_by"
        validated_data["topic"] = Topic.objects.get_or_create(
            subject_id=validated_data.pop("subject"),
            standard_id=validated_data.pop("standard"),
            name=validated_data.pop("topic"),
        )[0]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class TestSerializer(serializers.ModelSerializer):
    questions = serializers.IntegerField(source="question_count", read_only=True)
    topic_name = serializers.CharField(read_only=True)
    standard = serializers.IntegerField(read_only=False)
    subject = serializers.CharField(read_only=False)
    creator_name = serializers.CharField(read_only=True)
    total_score = serializers.IntegerField(read_only=True)
    section = serializers.CharField(read_only=True)

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "description",
            "section",
            "topic",
            "topic_name",
            "standard",
            "subject",
            "questions",
            "creator_name",
            "total_score",
            "updated_at",
        )


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = ("id", "name")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name")


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.ListField(child=serializers.CharField())
    marks = serializers.IntegerField(default=1)
    correct_option = serializers.IntegerField(default=0)

    class Meta:
        model = Question

        fields = (
            "id",
            "question",
            "options",
            "correct_option",
            "marks",
        )
