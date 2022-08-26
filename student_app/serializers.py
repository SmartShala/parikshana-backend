from rest_framework import serializers
from school_app.models import SchoolStudent


class StudentSerializer(serializers.ModelSerializer):
    # standard = serializers.IntegerField(
    #     source="school_class_students__school_class_standard__name"
    # )

    class Meta:
        model = SchoolStudent
        fields = (
            "id",
            "std_id",
            "name",
            "age",
            "image",
        )
