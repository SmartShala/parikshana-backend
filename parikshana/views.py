from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import render


class Home(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({"message": "Namaste,world"}, status=200)


def index(request):
    return render(request, "home.html")
