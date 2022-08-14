from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from parikshana.custom_errors import ExceptionMixin
from parikshana.custom_perms import IsAdminUser

from parikshana.custom_errors import (
    Http404,
    Http200,
    Http201,
    Http401,
    Http400,
    Http403,
)

from test_app.tasks import work


class TestApp(APIView):
    def get(self, request):
        res = work.apply_async(args=["John", "Doe"])
        print(res)
        return Response({"message": "hello world"})
