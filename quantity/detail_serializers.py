from rest_framework import serializers
from quantity.models import Quantity
from quantity.serializers import QuantitySerializer


class QuantityDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quantity
        fields = (
            'id', 'production', 'amount', 'plus_price', 'description', 'created_at', 'caption'
        )

    def create(self, validated_data):
        return Quantity.objects.create(**validated_data)
