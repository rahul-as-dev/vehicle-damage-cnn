from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from awsS3.utils import AwsHandler
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from login.models import Profile
from inspection.models import Inspection, Image
import json


@csrf_exempt
def post_to_s3(request):
    image = request.FILES['image']
    transactionId = request.POST['transactionId']
    extension = request.POST['extension']
    context = request.POST['context']
    aws_handler = AwsHandler(aws_access_key_id='AKIAVRNDGDHT7P3M5XUR',
                             aws_secret_access_key='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')
    response = aws_handler.upload_image_to_s3(image,object_name=transactionId+'/'+image.name)
    image = Image.objects.create(transaction_id=transactionId, context=context, extension=extension,
                                 etag=response['ETag'])
    data = {
        "status": "success",
        "error_msg": "image uploaded successfully"
    }
    return JsonResponse(data)


@csrf_exempt
def initiate_inspection(request):
    if request.method == 'POST' and request.user.is_authenticated:
        inspection = Inspection.objects.create(user=request.user,
                                               engineNumber=json.loads(request.body).get('engineNumber'),
                                               chassisNumber=json.loads(request.body).get('chassisNumber'),
                                               registrationNumber=json.loads(request.body).get('registrationNumber')
                                               )
        data = {
            "status": "success",
            "error_msg": "inspection initiated",
            "transactionId": inspection.transaction_id
        }
        return JsonResponse(data)
    return HttpResponse("401 unautherized")


@csrf_exempt
def process_inspection(request):
    if request.method == 'POST' and request.user.is_authenticated:
        transactionId=json.loads(request.body).get('transactionId')
        images = Image.objects.filter(transaction_id=transactionId);
        responses = []
        aws_handler = AwsHandler(aws_access_key_id='AKIAVRNDGDHT7P3M5XUR',
                                 aws_secret_access_key='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')
        for image in images:
            response = aws_handler.get_image_from_s3(image_key=transactionId+'/'+image.context,ETag=image.etag)
            responses.append(response)

        data ={}
        return JsonResponse(data)
    return HttpResponse("401 unautherized")