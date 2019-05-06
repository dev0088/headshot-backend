from rest_framework import serializers
from production.models import Production
from production.serializers import ProductionSerializer
from quantity.detail_serializers import QuantityDetailSerializer


class ProductionDetailSerializer(serializers.ModelSerializer):

    production_quantities = QuantityDetailSerializer(many=True)

    class Meta:
        model = Production
        fields = (
            'id', 'name', 'title', 'description', 
            'gallery_image', 'gallery_image_external_url', 
            'overview_image', 'overview_image_external_url', 
            'more_about',
            'price',
            'created_at',
            'production_quantities'
        )

    def create(self, validated_data):
        return Production.objects.create(**validated_data)

