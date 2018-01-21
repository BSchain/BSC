from django.shortcuts import render, render_to_response, get_list_or_404, get_object_or_404
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from BSCapp.models import *
from django.utils import timezone
import hashlib
from django.db import connection
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import time
from BSCapp.root_chain.utils import *
# Create your views here.

@csrf_exempt
def signUpCustom(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
    except Exception:
        return render(request, "../templates/app/signup.html")
    try:
        c = User.objects.get(user_name=username)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'username has been signed up',
            }))
    except Exception as e:
        # print(str(e))
        user_id = generate_uuid(username)
        User(user_id=user_id, user_name=username, user_pwd=password,
             user_email=email).save()
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))