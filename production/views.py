from authentication.models import User
from production.models import Production
from production.serializers import ProductionSerializer
from production.create_serializers import ProductionCreateSerializer
from production.detail_serializers import ProductionDetailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class ProductionList(APIView):
    """
    Retrieve all casting requests of client.
    """
    @swagger_auto_schema(responses={200: ProductionSerializer(many=True)})
    def get(self, request, format=None):
        productions = Production.objects.all()
        serializer = ProductionSerializer(productions, many=True)
        return Response(serializer.data)


class ProductionDetail(APIView):
    """
    Retrieve, update or delete a production.
    """
    def get_object(self, pk):
        try:
            return Production.objects.get(pk=pk)
        except Production.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: ProductionDetailSerializer(many=False)})
    def get(self, request, pk, format=None):
        production = self.get_object(pk)
        serializer = ProductionDetailSerializer(production)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductionCreateSerializer,
        responses={200: ProductionSerializer(many=False)}
    )
    def put(self, request, pk, format=None):
        production = self.get_object(pk)
        serializer = ProductionSerializer(production, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'OK'})
    def delete(self, request, pk, format=None):
        production = self.get_object(pk)
        production.delete()
        return Response({'id': int(pk)}, status=status.HTTP_200_OK)


class ProductionCreate(APIView):
    """
    Get a new production
    """
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=ProductionCreateSerializer,
                         responses={200: ProductionSerializer(many=False)})
    def post(self, request,format=None):
        serializer = ProductionCreateSerializer(data=request.data)

        if serializer.is_valid():
            new_production = Production(**serializer.validated_data)
            new_production.save()
            new_serializer = ProductionSerializer(new_production, many=False)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


