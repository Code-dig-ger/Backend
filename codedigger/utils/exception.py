from email.policy import default
from rest_framework import status
from rest_framework.exceptions import APIException


class ValidationException(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'status': 'FAILED', 'error': 'Bad Request.'}
    default_code = 'invalid'

    def __init__(self, detail=None, status_code=None, code=None):
        self.detail = self.default_detail if detail == None \
            else {'status': 'FAILED', 'error': detail}
        self.code = self.default_code if code == None \
            else code
        if status_code is not None:
            self.status_code = status_code        


class UnauthorizedException(APIException):

    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'not_authenticated'
    default_detail = {
        'status': 'FAILED',
        'error': 'Authentication credentials were not provided.'
    }

    def __init__(self, detail=None, status_code=None, code=None):
        self.detail = self.default_detail if detail == None \
            else {'status': 'FAILED', 'error': detail}
        self.code = self.default_code if code == None \
            else code
        if status_code is not None:
            self.status_code = status_code 


class ForbiddenException(APIException):

    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'permission_denied'
    default_detail = {
        'status': 'FAILED',
        'error': 'Permission Denied.'
    }

    def __init__(self, detail=None, status_code=None, code=None):
        self.detail = self.default_detail if detail == None \
            else {'status': 'FAILED', 'error': detail}
        self.code = self.default_code if code == None \
            else code
        if status_code is not None:
            self.status_code = status_code 
    

class NotFoundException(APIException):

    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'not_found'
    default_detail = {
        'status': 'FAILED',
        'error': 'Not Found.'
    }

    def __init__(self, detail=None, status_code=None, code=None):
        self.detail = self.default_detail if detail == None \
            else {'status': 'FAILED', 'error': detail}
        self.code = self.default_code if code == None \
            else code
        if status_code is not None:
            self.status_code = status_code 