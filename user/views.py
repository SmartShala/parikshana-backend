from rest_framework.views import APIView
from rest_framework import generics,permissions
from rest_framework.response import Response
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({
                "message":"Please Login"
            })
        serializer = UserSerializer(user)
        return Response(serializer.data,status=200)

