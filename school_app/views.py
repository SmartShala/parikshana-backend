from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

# from django_filters import *
from parikshana.custom_errors import ExceptionMixin
from parikshana.custom_perms import IsAdminUser
from .serializers import SchoolSerializer, TeacherSerializer
from .models import School, SchoolTeacher
from parikshana.custom_errors import (
    Http404,
    Http200,
    Http201,
    Http401,
    Http400,
    Http403,
)


# School Related APIS
# Requires Auth : Only admin users


class CreateSchool(generics.ListCreateAPIView, ExceptionMixin):
    """Hello world"""

    permission_classes = [IsAdminUser]
    serializer_class = SchoolSerializer

    def get_queryset(self):
        return School.objects.filter(
            deleted=False,
            created_by=self.request.user,
        ).order_by("created_at")


class UpdateDeleteSchool(generics.RetrieveUpdateAPIView, ExceptionMixin):
    permission_classes = [IsAdminUser]

    serializer_class = SchoolSerializer

    def get_object(self):
        try:
            return School.objects.get(id=self.kwargs["school_id"], deleted=False)
        except School.DoesNotExist or School.MultipleObjectsReturned:
            raise Http404("Invalid School ID Provided/No School Found!")
        except KeyError:
            raise Http400("Please Provide School ID")

    def delete(self):
        school = self.get_object()
        school.delete = True
        school.save()
        raise Http200("Deleted Successfully")


class AddGetTeachers(generics.ListCreateAPIView, ExceptionMixin):
    permission_classes = [IsAdminUser]
    serializer_class = TeacherSerializer
    filter_backends = [SearchFilter]

    def get_queryset(self):
        try:
            _params = self.request.query_params
            return (
                SchoolTeacher.objects.filter(
                    school=self.kwargs["school_id"],
                    school__deleted=False,
                )
                .prefetch_related("school_teacher_subjects", "school_teacher_standards")
                .select_related("school_teacher_teacher")
                .order_by("updated_at")
            )
        except KeyError:
            raise Http400("Please Provide School ID")


class UpdateDeleteTeachers(generics.RetrieveUpdateDestroyAPIView, ExceptionMixin):
    permission_classes = [IsAdminUser]
    serializer_class = TeacherSerializer

    def get_object(self):
        try:
            return SchoolTeacher.objects.get(
                id=self.kwargs["teacher_id"],
                school_id=self.kwargs["school_id"],
                school__deleted=False,
            )
        except SchoolTeacher.DoesNotExist or SchoolTeacher.MultipleObjectsReturned:
            raise Http404("Invalid Teacher ID Provided/No Teacher Found!")
        except KeyError:
            raise Http400("Please Provide School/Teacher ID")
