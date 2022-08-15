from rest_framework import serializers
from test_app.models import Test


class TestSerializer(serializers.ModelSerializer):
    questions = serializers.IntegerField(source="question_count", read_only=True)
    topic_name = serializers.CharField(read_only=True)
    standard = serializers.CharField(read_only=True)
    subject = serializers.CharField(read_only=True)
    creator_name = serializers.CharField(read_only=True)
    total_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "description",
            "topic",
            "topic_name",
            "standard",
            "subject",
            "questions",
            "creator_name",
            "total_score",
            "updated_at",
        )

    def create(self, validated_data):
        "Overloading to add created_by"
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
