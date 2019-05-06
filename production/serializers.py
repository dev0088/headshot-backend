from rest_framework import serializers
from .models import Production


class ProductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Production
        fields = (
            'id', 
            'name', 
            'title', 
            'description', 
            'gallery_image', 
            'gallery_image_external_url', 
            'overview_image', 
            'overview_image_external_url',
            'price',
            'more_about',
            'created_at'
        )


