from rest_framework import permissions
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class HasValidRefreshToken(permissions.BasePermission):
    message = "Refresh token is missing or invalid."

    def has_permission(self, request, view):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed(self.message)
        
        try:
            request.validated_refresh_token = RefreshToken(refresh_token)
            return True
        except TokenError:
            raise AuthenticationFailed(self.message)