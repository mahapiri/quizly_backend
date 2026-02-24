from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from auth_app.api.serializers import LoginSerializer, RegisterSerzializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerzializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = self.create_user(serializer.validated_data)

            token, created = Token.objects.get_or_create(user=user)

            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_user(self, validated_data):
        """
        Create a new user with the provided data.
        """
        try:
            created_user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"]
            )
            return created_user
        except Exception:
            raise Exception()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user is None:
                return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                "detail": "Login successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An internal server occurred.{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
























# class LoginView(ModelViewSet):
#     print("LoginView called")
#     pass


# class LogoutView(ModelViewSet):
#     print("LogoutView called")
#     pass


# class TokenRefreshView(ModelViewSet):
#     print("TokenRefreshView called")
#     pass