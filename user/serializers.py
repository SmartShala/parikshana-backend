from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import (
    make_password,
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "contact",
            "teacher_id",
            "password",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = User(**validated_data)
        # Hash the user's password.
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):

        super().update()
