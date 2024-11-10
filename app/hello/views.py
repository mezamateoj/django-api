from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .serializers import HelloSerializer
from rest_framework import viewsets

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
    


class HelloViewSet(viewsets.ViewSet):
    """
    Example viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    serializer_class = HelloSerializer

    # to register this view we use routers
    def list(self, request: Request):

        elements = [
            'Hello',
            'World',
            'From View Set'
        ]

        return Response({
            'message':'Hello View Set',
            'data': elements,
        }, status=status.HTTP_200_OK)
    
    def create(self, request: Request):
        """Create hello message"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            return Response({'message': f'Hello {name}'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def retrieve(self, request: Request, pk=None):
        """handle getting object by id"""
        return Response({'http method': 'GET'})


    def update(self, request: Request, pk=None):
        return Response({'http method': 'UPDATE'})
        

    def partial_update(self, request: Request, pk=None):
        return Response({'http method': 'PATCH'})


    def destroy(self, request: Request, pk=None):
        return Response({'http method': 'DELETE'})
    
