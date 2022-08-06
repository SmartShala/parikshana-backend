from rest_framework.views import APIView
from rest_framework import generics,permissions
from rest_framework.response import Response


class Home(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        return Response({
            "message":"Namaste,world"
        },status=200)
