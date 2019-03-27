import mimetypes
import json
import time
import os
import sys
from werkzeug.utils import secure_filename
from django.shortcuts import render
from django.http import Http404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from headshot.models import Headshot
from headshot.serializers import HeadshotSerializer
from headshot.create_serializers import HeadshotCreateSerializer
from headshot.detail_serializers import HeadshotDetailSerializer
from headshot.upload_serializers import HeadshotUploadSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import cloudinary
import cloudinary.uploader
import cloudinary.api


class HeadshotList(APIView):
    """
    Retrieve all headshot.
    """
    @swagger_auto_schema(responses={200: HeadshotSerializer(many=True)})
    def get(self, request, format=None):
        headshots = Headshot.objects.all()
        serializer = HeadshotSerializer(headshots, many=True)
        return Response(serializer.data)


class HeadshotDetail(APIView):
    """
    Retrieve, update or delete a headshot.
    """
    def get_object(self, pk):
        try:
            return Headshot.objects.get(pk=pk)
        except Headshot.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: HeadshotDetailSerializer(many=False)})
    def get(self, request, pk, format=None):
        headshot = self.get_object(pk)
        serializer = HeadshotDetailSerializer(headshot)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=HeadshotCreateSerializer,
        responses={200: HeadshotSerializer(many=False)}
    )
    def put(self, request, pk, format=None):
        headshot = self.get_object(pk)
        serializer = HeadshotSerializer(headshot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: 'OK'})
    def delete(self, request, pk, format=None):
        headshot = self.get_object(pk)
        headshot.delete()
        return Response({'id': int(pk)}, status=status.HTTP_200_OK)


class HeadshotCreate(APIView):
    """
    Get a new headshot
    """

    @swagger_auto_schema(request_body=HeadshotCreateSerializer,
                         responses={200: HeadshotSerializer(many=False)})
    def post(self, request, format=None):
        serializer = HeadshotCreateSerializer(data=request.data)

        if serializer.is_valid():
            new_headshot = Headshot(**serializer.validated_data)
            new_headshot.save()
            new_serializer = HeadshotSerializer(new_headshot, many=False)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HeadshotUpload(APIView):
    """
    Get a new headshot with uploaded image
    """
    parser_class = ( MultiPartParser, FormParser)
    # height = 500
    # width = 400
    # page_id = 1

    @swagger_auto_schema(request_body=HeadshotUploadSerializer,
                         responses={200: HeadshotDetailSerializer(many=False)})
    def put(self, request, pk, format=None):
        headshot = Headshot.objects.get(pk=pk)

        # serializer = HeadshotUploadSerializer(data=request.data)

        # if serializer.is_valid():
        if 'file' not in request.data:
            print("Empty content")
            return Response({'error': 'Empty content'}, status=status.HTTP_400_BAD_REQUEST)

        if not headshot:
            return Response({'error': 'Not found the headshot'}, status=status.HTTP_400_BAD_REQUEST)

        # Save temp file
        f = request.data['file']
        file_name = request.data['fileName']
        print('==== file: ', f)
        print('===================\n', file_name)
        # Upload image from frontend to cloudinary
        cloudinary.config( 
            cloud_name = "dnxe2ejbx", 
            api_key = "531987746948979", 
            api_secret = "mAG_-w5YQXBqUrvd5umM42QCyvI" 
        )

        res = cloudinary.uploader.upload(f)

        headshot.public_id = res['public_id']
        headshot.signature = res['signature']
        headshot.image_format = res['format']
        headshot.width = res['width']
        headshot.height = res['height']
        headshot.cloudinary_image_url = res['url']
        headshot.cloudinary_image_secure_url = res['secure_url']
        headshot.save()
        new_serializer = HeadshotSerializer(headshot)

        return Response(new_serializer.data, status=status.HTTP_200_OK)
        # return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        
