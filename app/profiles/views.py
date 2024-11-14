from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import viewsets
from .permissions import UpdateProfile
from rest_framework.authentication import TokenAuthentication


class Profile(APIView):
    """ """

    def post(self, request: Request):
        serializer = UserProfileSerializer(data=request.data)
        print(f'serializer: {serializer}')

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'user': UserProfileSerializer(user).data,
                    'message': 'Profile created successfully',
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateProfile,)

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
