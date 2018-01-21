from django.shortcuts import render, render_to_response, get_list_or_404, get_object_or_404
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from BSCapp.models import *
from django.utils import timezone
import hashlib
from django.db import connection
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from time import time
from BSCapp.root_chain.utils import *
import BSCapp.root_chain.transaction as TX
# Create your views here.


@csrf_exempt
def signUp(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
    except Exception:
        return render(request, "app/signup.html")
    try:
        c = User.objects.get(user_id=username)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'username has been signed up',
            }))
    except Exception as e:
        print(str(e))
        user_id = generate_uuid(name=username)
        User(user_id=user_id, user_name=username, user_pwd=password,
               user_email=email).save()
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))

@csrf_exempt
def signIn(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return render(request, "app/signin.html")
    try:
        e = User.objects.get(user_id=username)
    except Exception:
        return HttpResponse(json.dumps({
        'statCode': -2,
        'errormessage': 'username or mail not exists',
        }))
    if(password != e.user_pwd):
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
