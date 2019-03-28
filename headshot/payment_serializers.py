from rest_framework import serializers
from headshot.models import Headshot


class HeadshotPaymentSerializer(serializers.Serializer):
    token = serializers.JSONField()
    amount = serializers.IntegerField()

    # class Meta:
    #     model = Headshot
    #     fields = (
    #         'id', 'email', 'file_name', 'cloudinary_image_url', 'quantity', 'status'
    #     )

    # def create(self, validated_data):
    #     return Headshot.objects.create(**validated_data)

