from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .serializers import HelloSerializer


class HelloView(APIView):

    serializer_class = HelloSerializer

    def get(self, request: Request, format=None):
        return Response({'method': 'GET'})

    
    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')

            return Response({'message': name}, status=status.HTTP_200_OK)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

    def put(self, request: Request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})
    

    def patch(self, request: Request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})
        

    def delete(self, request: Request, pk=None):
        """Delete and object"""
        return Response({'message': 'DELETE'})