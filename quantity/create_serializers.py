from rest_framework import serializers
from quantity.models import Quantity


class QuantityCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quantity
        fields = (
            'id', 'production', 'amount', 'plus_price', 'description', 'created_at'
        )

    def create(self, validated_data):
        return Quantity.objects.create(**validated_data)

