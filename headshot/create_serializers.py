from rest_framework import serializers
from headshot.models import Headshot


class HeadshotCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Headshot
        fields = (
            'id', 'email', 'file_name', 'cloudinary_image_url', 'quantity', 'status'
        )

    def create(self, validated_data):
        return Headshot.objects.create(**validated_data)

