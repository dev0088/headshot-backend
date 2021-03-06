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
            'doc_public_id',
            'doc_signature',
            'doc_format',
            'doc_size',
            'doc_url',
            'doc_secure_url',
            'doc_preview_url',
            'doc_preview_secure_url',
            'updated_at', 
            'created_at'
        )


