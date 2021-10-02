from rest_framework.response import Response
from rest_framework import status

def response(Data, Status = status.HTTP_200_OK):

    return Response(
        data= {
            'status': 'OK',
            'result': Data
        },
        status= Status
    )