from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # model we want to use as base for this Serializer
        model = get_user_model()
        # fields that we want to make accessible via the API
        fields = ('email', 'password', 'name')
        # extra restrictions for our fields variable
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
