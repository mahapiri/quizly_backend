import token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from auth_app.api.permissions import HasValidRefreshToken
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

            refresh = RefreshToken.for_user(user) #production secure=True setzen
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                "detail": "Login successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }

            response = Response(response_data, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=15 * 60
            )

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=7 * 24 * 60 * 60
            )

            return response
        except Exception as e:
            return Response({"error": f"An internal server occurred.{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")

        if not refresh:
            response = Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except TokenError:
            pass
        except Exception as e:
            return Response({"error": f"An internal server occurred.{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class TokenRefreshView(generics.GenericAPIView):
    permission_classes = [HasValidRefreshToken]

    def post(self, request, *args, **kwargs):
        try: 
            refresh = request.validated_refresh_token
            access_token = str(refresh.access_token)

            response = Response(
                {"detail": "Token refreshed"},
                status=status.HTTP_200_OK
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=15 * 60
            )
            return response
        except Exception as e:
            return Response({"error": f"An internal server occurred.{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    