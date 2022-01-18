from rest_framework.permissions import BasePermission, SAFE_METHODS
from user.models import Profile
from .exception import (ValidationException, UnauthorizedException, 
                        ForbiddenException)


class AuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user or \
            request.user.is_authenticated or \
                request.method in SAFE_METHODS:
            return True
        else:
            raise UnauthorizedException


class Authenticated(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise UnauthorizedException
        else:
            return True


class AuthenticatedAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        else:
            raise ForbiddenException


class AuthenticatedActivated(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if Profile.objects.get(owner=request.user).codeforces is not None:
                return True
            else:
                raise ValidationException('Account was not activated.')
        else:
            raise UnauthorizedException


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
