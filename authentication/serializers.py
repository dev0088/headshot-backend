from rest_framework import serializers

from .models import User


class GeneralUserSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'image', 'phone_number', 'overview']

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)


    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token', 'first_name', 'last_name']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        user = User.objects.create_user(**validated_data)
        return user

class UserReviewsSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'image', 'email', 'phone_number']
