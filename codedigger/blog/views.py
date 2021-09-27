from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, status

from .models import Blog
from .serializers import BlogSerializer, ABlogSerializer
from user.permissions import *


class BlogAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = BlogSerializer
    #passed_id = None
    # running queries and stuff

    def get(self, request):
        return Response({'status': 'OK', 'result': BlogSerializer(
            Blog.objects.all(), many=True).data})


class ABlogAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = [AuthenticatedOrReadOnly]
    #authentication_classes = [SessionAuthentication]
    serializer_class = ABlogSerializer
    #passed_id = None

    # running queries and stuff
    def get(self, request, slug):

        qs = Blog.objects.filter(slug=slug)
        if qs.exists():
            return Response({'status': 'OK',
                             'result': ABlogSerializer(qs[0]).data})
        else:
            return Response({'status': 'FAILED',
                             'error': 'Requested Blog doesn\'t exists.'},
                            status=status.HTTP_400_BAD_REQUEST)
