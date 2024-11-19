from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from .serializers import UserProfileSerializer, AuthTokenSerializer, ProfileFeedSerializer
from .models import UserProfile, ProfileFeedItem
from rest_framework import viewsets
from .permissions import UpdateProfile, UpdateUserFeed
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


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

    # permission so we can update other users, etc.
    authentication_classes = [TokenAuthentication]
    permission_classes = [UpdateProfile]

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    # query using /?search=name
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user auth tokens"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        # pass email and pass as body
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {'token': token.key, 'user_id': user.pk, 'email': user.email, 'name': user.name}
        )


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""

    # only auth users can view this endpoint
    authentication_classes = [TokenAuthentication]
    # the isAuth will make sure only users with header: Authorization: Token thetoken
    # can view the info
    permission_classes = [UpdateUserFeed, IsAuthenticated]

    serializer_class = ProfileFeedSerializer
    queryset = ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets the user profile to logged in user"""
        print('reques', self.request)
        # if user is auth then the request add this .user field from the request
        serializer.save(user_profile=self.request.user)
