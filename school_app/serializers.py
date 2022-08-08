from rest_framework import serializers
from school_app.models import School, SchoolClass, SchoolTeacher, SchoolStudent
from test_app.models import Subject, Standard


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            "id",
            "created_by",
            "name",
            "description",
            "created_by",
            "created_at",
        )
        read_only_fields = ("id",)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="teacher")
    school_id = serializers.IntegerField(source="school")
    name = serializers.CharField(source="teacher.name", max_length=100)
    subjects = SubjectSerializer(many=True, read_only=True)
    standards = StandardSerializer(many=True, read_only=True)

    class Meta:
        model = SchoolTeacher
        fields = (
            "id",
            "school_id",
            "user_id",
            "name",
            "description",
            "subjects",
            "standards",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "subjects", "standards", "user", "name")
