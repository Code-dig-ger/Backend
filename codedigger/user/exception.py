from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class ValidationException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Custom Exception Message"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = {
            'status' : "FAILED",
            'error' : detail
        }
        if status_code is not None:
            self.status_code = status_code

class AuthenticationException(PermissionDenied):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Custom Exception Message"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = {
            'status' : "FAILED",
            'error' : detail
        }
        if status_code is not None:
            self.status_code = status_code 

class NotFoundException(PermissionDenied):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Custom Exception Message"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = {
            'status' : "FAILED",
            'error' : detail
        }
        if status_code is not None:
            self.status_code = status_code