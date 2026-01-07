from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from auth_app.api.serializers import RegisterSerzializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerzializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "User created successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(ModelViewSet):
#     print("LoginView called")
#     pass


# class LogoutView(ModelViewSet):
#     print("LogoutView called")
#     pass


# class TokenRefreshView(ModelViewSet):
#     print("TokenRefreshView called")
#     pass