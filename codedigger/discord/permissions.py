from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.permissions import BasePermission

from user.permissions import Forbidden


class ForbiddenBot(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        "status": "FAILED",
        "error": "Only Bots can access this page"
    }


class AuthenticatedBot(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_bot:
                return True
            else:
                raise ForbiddenBot
        else:
            raise Forbidden
