from rest_framework import serializers
from headshot.models import Headshot
from headshot.serializers import HeadshotSerializer
from quantity.detail_serializers import QuantityDetailSerializer


class HeadshotDetailSerializer(serializers.ModelSerializer):

    quantity = QuantityDetailSerializer(many=False)

    class Meta:
        model = Headshot
        fields = (
            'id', 
            'email', 
            'file_name', 
            'quantity', 
            'status', 
            'cloudinary_image_url', 
            'cloudinary_image_secure_url',
            'image_format', 
            'width', 
            'height', 
            'public_id', 
            'signature',
            'updated_at', 
            'created_at'
        )

    def create(self, validated_data):
        return Headshot.objects.create(**validated_data)

