from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS,AllowAny,  IsAuthenticated, DjangoModelPermissions, BasePermission
from .serializers import CountSerializer
from counteye.models import Count
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
# from django.shortcuts import render

class PermissionUserCount(BasePermission):
    message = 'Somente autores do envio'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class CountList(generics.ListAPIView):
    # permission_classes = [AllowAny]
    serializer_class = CountSerializer
    queryset = Count.postobjects.all()

    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(Count, slug=item)

    # def get_queryset(self):
    #     return Count.objects.all()

# class CountList(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = Count.postobjects.all()
#     serializer_class = CountSerializer

class CountDetail(generics.RetrieveAPIView):
    serializer_class = CountSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Count, slug=item)

# class CountDetail(generics.RetrieveUpdateDestroyAPIView, PermissionUserCount ): #RetrieveDestroyAPIView?
#     permission_classes = [AllowAny]
#     queryset = Count.objects.all()
#     serializer_class = CountSerializer

class CreateCount(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

class AdminCountDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

class EditCount(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

class DeleteCount(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Count.objects.all()
    serializer_class = CountSerializer

