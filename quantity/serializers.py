from rest_framework import serializers
from .models import Quantity


class QuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Quantity
        fields = (
            'id', 'production', 'amount', 'plus_price', 'description', 'created_at'
        )


