from rest_framework import serializers
from production.models import Production


class ProductionCreateSerializer(serializers.ModelSerializer):

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
            'price',
            'overview_image_external_url', 
            'more_about'
        )

    def create(self, validated_data):
        return Production.objects.create(**validated_data)

