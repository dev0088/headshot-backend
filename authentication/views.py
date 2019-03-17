from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, GeneralUserSerializer, UserReviewsSerializer
from .models import User

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'username': request.data.get('username'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'overview': request.data.get('overview')
        }
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Create talent
        # user_instance = User.objects.get(username=user['username'])
        # if not user_instance:
        #     talent = Talent.objects.create(user=user_instance.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UsersList(APIView):
    """
    List all talent pictures.
    """

    def get(self, request, format=None):
        users = User.objects.filter(is_superuser=False)
        serializer = GeneralUserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    """
    Retrieve a talent_position_type_item instance.
    """
    def get_object(self, pk):
        try:
            return TalentPositionType.objects.get(pk=pk)
        except TalentPositionType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        talent_position_type_item = self.get_object(pk)
        serializer = TalentPositionTypeSerializer(talent_position_type_item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        talent_position_type_item = self.get_object(pk)
        serializer = TalentPositionTypeSerializer(talent_position_type_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        talent_position_type_item = self.get_object(pk)
        talent_position_type_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserReviewsList(APIView):
    """
    List all user reviews.
    """

    def get(self, request, format=None):
        users = User.objects.filter(is_superuser=False)
        serializer = UserReviewsSerializer(users, many=True)
        return Response(serializer.data)
