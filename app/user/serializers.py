"""
    serializer for user API

"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from django.utils.translation import gettext as _


from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password','name']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it
        """
        user = get_user_model().objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        """
        Update a user, setting the password correctly and returning it
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        return super().update(instance, validated_data)
    
    
    
class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user authentication token
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user
        """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs