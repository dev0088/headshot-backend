import mimetypes
import json
import time
import os
import sys
import json
from werkzeug.utils import secure_filename
from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import cloudinary
import cloudinary.uploader
import cloudinary.api
import stripe
from headshot.models import Headshot
from headshot.serializers import HeadshotSerializer
from headshot.create_serializers import HeadshotCreateSerializer
from headshot.detail_serializers import HeadshotDetailSerializer
from headshot.upload_serializers import HeadshotUploadSerializer
from headshot.payment_serializers import HeadshotPaymentSerializer
from stripe_payment.models import StripePayment
from converter.text2pdf import text_to_image
from converter.pdf2jpg import pdf_to_image
from converter.doc2pdf import doc_to_pdf, docx_to_pdf

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.log = 'info'  # or 'debug'


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

    @swagger_auto_schema(
        request_body=HeadshotCreateSerializer,
        responses={200: HeadshotSerializer(many=False)}
    )
    def post(self, request, format=None):
        serializer = HeadshotCreateSerializer(data=request.data)

        if serializer.is_valid():
            new_headshot = Headshot(**serializer.validated_data)
            new_headshot.save()
            new_serializer = HeadshotSerializer(new_headshot, many=False)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HeadshotUploadImage(APIView):
    """
    Get a new headshot with uploaded image
    """
    parser_class = ( MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=HeadshotUploadSerializer,
        responses={200: HeadshotDetailSerializer(many=False)}
    )
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
        # file_name = request.data['fileName']
        # Upload image from frontend to cloudinary
        cloudinary.config( 
            cloud_name = "dnxe2ejbx", 
            api_key = "531987746948979", 
            api_secret = "mAG_-w5YQXBqUrvd5umM42QCyvI" 
        )

        res = cloudinary.uploader.upload(f, folder = 'Headshots')

        headshot.public_id = res['public_id']
        headshot.signature = res['signature']
        headshot.image_format = res['format']
        headshot.width = res['width']
        headshot.height = res['height']
        headshot.cloudinary_image_url = res['url']
        headshot.cloudinary_image_secure_url = res['secure_url']
        headshot.status = 'Required'
        headshot.save()
        new_serializer = HeadshotSerializer(headshot)

        return Response(new_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=HeadshotUploadSerializer,
        responses={200: HeadshotDetailSerializer(many=False)}
    )
    def post(self, request, pk, format=None):
        headshot = Headshot.objects.get(pk=pk)

        # if serializer.is_valid():
        if 'file' not in request.data:
            print("Empty content")
            return Response({'error': 'Empty content'}, status=status.HTTP_400_BAD_REQUEST)

        if not headshot:
            return Response({'error': 'Not found the headshot'}, status=status.HTTP_400_BAD_REQUEST)

        # Save temp file
        f = request.data['file']
        # file_name = request.data['fileName']
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
        headshot.status = 'Required'
        headshot.save()
        new_serializer = HeadshotSerializer(headshot)

        return Response(new_serializer.data, status=status.HTTP_200_OK)


class HeadshotUploadDoc(APIView):

    parser_class = (MultiPartParser, FormParser)

    def convert_pdf_to_image(self, cach_dir_path, file_path):
        return pdf_to_image(cach_dir_path, file_path)

    def convert_text_to_png(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        image_file_name = '{file_name}{extension}'.format(
                file_name = file_name,
                extension = '.png'
            )
        image = text_to_image(file_path)
        image.save(image_file_name)
        return image_file_name

    def convert_doc_to_pdf(self, file_path):
        preview = doc_to_pdf(file_path)
        return preview

    def convert_docx_to_pdf(self, file_path):
        preview = docx_to_pdf(file_path)
        return preview

    @swagger_auto_schema(request_body=HeadshotUploadSerializer,
                         responses={200: HeadshotDetailSerializer(many=False)})
    def put(self, request, pk, format=None):
        headshot = Headshot.objects.get(pk=pk)
        if 'file' not in request.data:
            print("Empty content")
            return Response({'error': 'Empty content'}, status=status.HTTP_400_BAD_REQUEST)

        if not headshot:
            return Response({'error': 'Not found the headshot'}, status=status.HTTP_400_BAD_REQUEST)

        # Save temp file
        file_data = request.data['file']
        file_type = request.data['type']
        print('==== file: ', file_data)
        cloudinary.config( 
            cloud_name = "dnxe2ejbx", 
            api_key = "531987746948979", 
            api_secret = "mAG_-w5YQXBqUrvd5umM42QCyvI" 
        )

        # Convert doc file to preview image and Upload it to Cloudinary
        file_ext = ''
        if file_type == 'text/plain':
            file_ext = 'txt'
        elif file_type == 'application/pdf':
            file_ext = 'pdf'
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            file_ext = 'docx'
        elif file_type == 'application/msword':
            file_ext = 'doc'
        
        file_name = 'headshot_{id}.{ext}'.format(id=headshot.id, ext=file_ext) 
        tmp_file_dir = 'temp'
        tmp_file_path = '{tmp_file_dir}/{file_name}'.format(
                tmp_file_dir = tmp_file_dir,
                file_name = file_name
            )
        stored_path = default_storage.save(tmp_file_path, ContentFile(file_data.read()))
        
        # Generate preview file in image file
        media_root = settings.MEDIA_ROOT
        full_dir = os.path.join(media_root, tmp_file_dir) + '/'
        full_path = os.path.join(media_root, stored_path)
        print('===== : ', file_name, tmp_file_path, full_dir, full_path )

        # Get extension
        _, file_extension = os.path.splitext(stored_path)
        if sys.platform == 'darwin':
            if file_extension == '.txt':
                preview = self.convert_text_to_png(full_path)
            elif file_extension == '.doc':
                preview = self.convert_doc_to_pdf(full_path)
                print ('==== doc: preview: ', preview)
                preview = self.convert_pdf_to_image(full_dir, preview)
            elif file_extension == '.docx':
                preview = self.convert_docx_to_pdf(full_path)
                print ('==== docx: preview: ', preview)
                preview = self.convert_pdf_to_image(full_dir, preview)
            elif file_extension == '.pdf':
                preview = self.convert_pdf_to_image(full_dir, full_path)
        else:
            preview = self.convert_pdf_to_image(full_dir, full_path)

        tmp = preview.split('/')
        preview_file_name = tmp[len(tmp) - 1]
        preview_file_path = os.path.join('media', tmp_file_dir, preview_file_name)
        # Upload doc preview file to Cloudinary
        res_preview = cloudinary.uploader.upload(preview_file_path, folder = 'Docs')
        print ('==== res_preview: ', res_preview)
        # Upload doc file to Cloudinary
        res = cloudinary.uploader.upload(
            full_path, 
            folder = 'Docs',
            resource_type = 'raw',
            allowed_formats='txt, pdf, doc, docx'
        )

        # Save every info into database
        headshot.doc_public_id = res['public_id']
        headshot.doc_signature = res['signature']
        headshot.doc_format = file_type
        headshot.doc_url = res['url']
        headshot.doc_secure_url = res['secure_url']
        headshot.doc_preview_url = res_preview['url']
        headshot.doc_preview_secure_url = res_preview['secure_url']
        
        headshot.status = 'Required'
        headshot.save()
        new_serializer = HeadshotSerializer(headshot)

        return Response(new_serializer.data, status=status.HTTP_200_OK)


class HeadshotPayment(APIView):
    """
    Create payment for a headshot
    """

    def checkout(self, token, amount, headshot):
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='USD',
                source=token['id'],
                description='{user} charge to print {file_name} on {image_url}'.format(
                    user=headshot.email,
                    file_name=headshot.file_name,
                    image_url=headshot.cloudinary_image_secure_url
                ),
                statement_descriptor='headshot_id: {headshot_id}.'.format(
                    headshot_id=headshot.id
                ),
                # metadata={'order_id': 12345}
            )

            # Only confirm an order after you have status: succeeded
            print("______STATUS_____", charge['status'])  # should be succeeded
            if charge['status'] == 'succeeded':
                return Response({'message': 'Your transaction has been successful.'})
            else:
                raise stripe.error.CardError
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            print('Status is: %s' % e.http_status)
            print('Type is: %s' % err.get('type'))
            print('Code is: %s' % err.get('code'))
            print('Message is %s' % err.get('message'))
            return Response(
                {"message": err.get('message')},
                status=e.http_status
            )
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return Response(
                {'message': "The API was not able to respond, try again."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        except stripe.error.InvalidRequestError as e:
            # invalid parameters were supplied to Stripe's API
            return Response(
                {'message': "Invalid parameters, unable to process payment."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return Response(
                {'message': 'Network communication failed, try again.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe
            # send yourself an email
            return Response(
                {'message': 'Internal Error, contact support.'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Something else happened, completely unrelated to Stripe
        except Exception as e:
            return Response(
                {'message': 'Unable to process payment, try again.'}, 
                status=status.HTTP_403_FORBIDDEN
            )

    def create_customer(self, headshot, stripe_payment, amount):
        customer = stripe.Customer.create(
            email='paying.user@example.com',
            source=stripe_payment.source,
        )
        print('==== customer: ', customer)
        stripe_payment.customer_id = customer.id
        stripe_payment.save()


    @swagger_auto_schema(request_body=HeadshotPaymentSerializer,
                         responses={200: HeadshotDetailSerializer(many=False)})
    def post(self, request, pk, format=None):
        headshot = Headshot.objects.get(pk=pk)
        # if serializer.is_valid():
        if 'token' not in request.data:
            return Response({'error': 'Empty token'}, status=status.HTTP_400_BAD_REQUEST)

        if 'amount' not in request.data:
            return Response({'error': 'Empty amount'}, status=status.HTTP_400_BAD_REQUEST)

        if not headshot:
            return Response({'error': 'Not found the headshot'}, status=status.HTTP_400_BAD_REQUEST)

        token = request.data['token']
        amount = request.data['amount']
        card = token['card']

        new_stripe_payment = StripePayment.objects.create(headshot_id=headshot.id)
        new_stripe_payment.token_id = token['id']
        new_stripe_payment.source = token['id']
        new_stripe_payment.card_id = card['id']
        new_stripe_payment.address_city = card['address_city'] if card['address_city'] else ''
        new_stripe_payment.address_country = card['address_country'] if card['address_country'] else ''
        new_stripe_payment.address_line1 = card['address_line1'] if card['address_line1'] else ''
        new_stripe_payment.address_line1_check = card['address_line1_check'] if card['address_line1_check'] else ''
        new_stripe_payment.address_line2 = card['address_line2'] if card['address_line2'] else ''
        new_stripe_payment.address_state = card['address_state'] if card['address_state'] else ''
        new_stripe_payment.address_zip = card['address_zip'] if card['address_zip'] else ''
        new_stripe_payment.address_zip_check = card['address_zip_check'] if card['address_zip_check'] else ''
        new_stripe_payment.brand = card['brand'] if card['brand'] else ''
        new_stripe_payment.exp_month = card['exp_month']
        new_stripe_payment.exp_year = card['exp_year']
        new_stripe_payment.last4 = card['last4'] if card['last4'] else ''
        new_stripe_payment.livemode = token['livemode']
        new_stripe_payment.amount = amount
        new_stripe_payment.save()
        
        headshot.status="Required"
        headshot.save()



        # Create stripe payment
        return self.checkout(token, amount, headshot)
        
