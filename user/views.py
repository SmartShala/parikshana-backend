from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView,generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    paginaton_class = None

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "Please Login"})
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

class UpdatePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserUpdateSerializer
    
