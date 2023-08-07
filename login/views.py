import random
from login.utils import MessageHandler
from django.shortcuts import render
from .models import *
from django.contrib.auth import login,logout
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@csrf_exempt
def login_request(request):
    if(request.method == 'POST'):
        phone_number =json.loads(request.body).get('phone_number')
        profile =Profile.objects.filter(phone_number=phone_number)
        if not profile.exists():
            user=User.objects.create_user(username=phone_number)
            profile=Profile.objects.create(user=user,phone_number=phone_number)
            profile.save()
        else:
            profile=profile[0]
        profile.otp=random.randint(1000,9999)
        profile.save()
        message_handler = MessageHandler(phone_number,profile.otp).send_otp()
        data = {
            "status": "success",
            "error_msg": "OTP Sent Successfully"
        }
        return JsonResponse(data)

@csrf_exempt
def verify_otp(request):
    if(request.method =='POST'):

        otp= json.loads(request.body).get('otp')
        phone_number = json.loads(request.body).get('phone_number')
        print(otp,phone_number)
        profile =Profile.objects.get(phone_number= phone_number)
        print(profile.otp)
        if otp == profile.otp:
            login(request,profile.user)
            data = {
                "status": "success",
                "error_msg": "logged in Successfully"
            }
            return JsonResponse(data)

    return HttpResponse("error")
@csrf_exempt
def logout_request(request):
    if(request.method == 'POST'):
        data = {
            "status": "success",
            "error_msg": "logged out Successfully"
        }
        return JsonResponse(data)

