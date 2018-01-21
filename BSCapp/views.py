from django.shortcuts import render, render_to_response, get_list_or_404, get_object_or_404
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from BSCapp.models import *
from django.utils import timezone
import hashlib
from django.db import connection
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from BSCapp.root_chain.utils import *
from BSCapp.root_chain.transaction import *
import time
import random
# Create your views here.

@csrf_exempt
def getIndex(request):
    request.session['username'] = ""
    return render(request, "app/index.html")

@csrf_exempt
def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return render(request, "app/page-login.html")
    try:
        u = User.objects.get(user_name=username)
    except Exception:
        return HttpResponse(json.dumps({
        'statCode': -2,
        'errormessage': 'username or mail not exists',
        }))
    if(password != u.user_pwd):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': 'wrong password',
            }))
    else:
        request.session['username'] = username
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))

@csrf_exempt
def signUp(request):
    try:
        user_name = request.POST['username']
        user_pwd = request.POST['password']
        user_email = request.POST['email']
        user_id = generate_uuid(user_name)
        print(user_id)
    except Exception as e:
        print(str(e))
        return render(request, "app/page-signup.html")
    try:
        c = User.objects.get(user_name=user_name)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'username has been signed up',
            }))
    except Exception as e:
        User(user_id=user_id, user_name=user_name,
            user_pwd=user_pwd, user_email=user_email).save()
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': user_name,
            }))

@csrf_exempt
def userInfo(request):
    user_name = request.session['username']
    return render(request, "app/userInfo.html")
