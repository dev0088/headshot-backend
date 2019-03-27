from rest_framework import serializers
from .models import Headshot


class HeadshotSerializer(serializers.ModelSerializer):

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


