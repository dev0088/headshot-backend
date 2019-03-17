from authentication.models import User
from quantity.models import Quantity
from quantity.serializers import QuantitySerializer
from quantity.create_serializers import QuantityCreateSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class QuantityList(APIView):
    """
    Retrieve all quantities.
    """
    @swagger_auto_schema(responses={200: QuantitySerializer(many=True)})
    def get(self, request, format=None):
        quantitys = Quantity.objects.all()
        serializer = QuantitySerializer(quantitys, many=True)
        return Response(serializer.data)


class QuantityDetail(APIView):
    """
    Retrieve, update or delete a quantity.
    """
    def get_object(self, pk):
        try:
            return Quantity.objects.get(pk=pk)
        except Quantity.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: QuantitySerializer(many=False)})
    def get(self, request, pk, format=None):
        quantity = self.get_object(pk)
        serializer = QuantitySerializer(quantity)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=QuantityCreateSerializer,
        responses={200: QuantitySerializer(many=False)}
    )
    def put(self, request, pk, format=None):
        quantity = self.get_object(pk)
        serializer = QuantitySerializer(quantity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'OK'})
    def delete(self, request, pk, format=None):
        quantity = self.get_object(pk)
        quantity.delete()
        return Response({'id': int(pk)}, status=status.HTTP_200_OK)


class QuantityCreate(APIView):
    """
    Create a new quantity
    """
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=QuantityCreateSerializer,
                         responses={200: QuantitySerializer(many=False)})
    def post(self, request,format=None):
        serializer = QuantityCreateSerializer(data=request.data)

        if serializer.is_valid():
            new_quantity = Quantity(**serializer.validated_data)
            new_quantity.save()
            new_serializer = QuantitySerializer(new_quantity, many=False)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


