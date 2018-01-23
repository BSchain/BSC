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
import BSCapp.root_chain.transaction as TX
from time import time

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
        a = Admin.objects.get(admin_name=username)
        if (password != a.admin_pwd):
            return HttpResponse(json.dumps({
                        'statCode': -3,
                        'errormessage': 'wrong password',
                        }))
        else:
            tx = TX.Transaction()
            tx.new_transaction(in_coins=[], out_coins=[],timestamp=time(), action='login',
                               seller=a.admin_id, buyer='',data_uuid='',credit=0.0, reviewer='')
            tx.save_transaction()

            request.session['username'] = username
            return HttpResponse(json.dumps({
                'statCode': 0,
                'username': username,
                }))
    except Exception:
        pass

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
        """

        :param in_coins:
        :param out_coins:
        :param timestamp:
        :param action:
        :param seller:
        :param buyer:
        :param data_uuid:
        :param credit:
        :param reviewer:
        :return:
        """

        tx = TX.Transaction()
        tx.new_transaction(in_coins=[], out_coins=[],timestamp=time(), action='login',
                           seller=u.user_id, buyer='',data_uuid='',credit=0.0, reviewer='')
        tx.save_transaction()

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
        c = Admin.objects.get(admin_name=user_name)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'username has been signed up',
            }))
    except Exception:
        pass
    try:
        c = User.objects.get(user_name=user_name)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'username has been signed up',
            }))
    except Exception as e:
        User(user_id=user_id, user_name=user_name,
            user_pwd=user_pwd, user_email=user_email).save()
        Wallet(user_id=user_id, account = 0.0).save()
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': user_name,
            }))

@csrf_exempt
def userInfo(request):
    adminname = request.session['username']
    try:
        admin = User.objects.get(admin_name=adminname)
    except Exception:
        return render(request, "app/page-login.html")
    try:
        admin.admin_realName = request.POST['realname']
        admin.admin_email = request.POST['email']
        admin.admin_phone = request.POST['phone']
        admin.admin_idcard = request.POST['idcard']
        admin.admin_company = request.POST['company']
        admin.admin_title = request.POST['title']
        admin.admin_addr = request.POST['addr']
        admin.save()
        return HttpResponse(json.dumps({
            'statCode': 0
            }))
    except Exception as e:
        print(str(e))
        return render(request, "app/adminInfo.html",{
            'id': admin.admin_name,
            'name': admin.admin_realName,
            'email':admin.admin_email,
            'addr':admin.admin_addr,
            'phone':admin.admin_phone,
            'idcard':admin.admin_idcard,
            'company':admin.admin_company,
            'title':admin.admin_title,
            })

@csrf_exempt
def adminInfo(request):
    adminname = request.session['username']
    try:
        admin = Admin.objects.get(admin_name=adminname)
    except Exception:
        return render(request, "app/page-login.html")
    try:
        admin.admin_id = request.POST['admin_id']
        admin.admin_name = request.POST['admin_name']
        admin.save()
        return HttpResponse(json.dumps({
            'statCode': 0
            }))
    except Exception as e:
        print(str(e))
        return render(request, "app/adminInfo.html",{
            'id': admin.admin_id,
            'name': admin.admin_name
            })
