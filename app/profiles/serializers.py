from rest_framework import serializers
from .models import UserProfile, ProfileFeedItem
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserProfileSerializer(serializers.ModelSerializer):
    # this sets to point to the model
    # also set the field that we will make available
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        """Create and return a new user"""
        user = UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,  # Django uses username internally
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class ProfileFeedSerializer(serializers.ModelSerializer):
    """Serializer profile feed items"""

    class Meta:
        model = ProfileFeedItem
        # id, and created on are read only
        # we should make also user_profile read only so only the own user can edit profile
        # fields = ('id', 'user_profile', 'status_text', 'created_on')
        fields = '__all__'
        extra_kwargs = {'user_profile': {'read_only': True}}
