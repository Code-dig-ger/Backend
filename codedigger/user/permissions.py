from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Profile

class AuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user or request.user.is_authenticated or request.method in SAFE_METHODS:
            return True
        else:
            raise Forbidden
    

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class Forbidden(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'status' : "FAILED",
        'error':'Authentication credentials were not provided'
    }

class Authenticated(permissions.BasePermission):

    def has_permission(self,request,view):
        if not request.user or not request.user.is_authenticated:
            raise Forbidden
        else :
            return True

class ForbiddenActivation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'status' : "FAILED",
        'error': 'Account was not activated'
    }

class AuthenticatedActivated(permissions.BasePermission):

    def has_permission(self,request,view):
        if request.user and request.user.is_authenticated:
            if Profile.objects.get(owner = request.user).codeforces is not None:
                return True
            else:
                raise ForbiddenActivation
        else :
            raise Forbidden