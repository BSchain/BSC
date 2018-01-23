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
                'isAdmin': 1,
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
            'isAdmin': 0,
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
    # client cannot overwrite admin users
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
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    try:
        user.user_realName = request.POST['realname']
        user.user_email = request.POST['email']
        user.user_phone = request.POST['phone']
        user.user_idcard = request.POST['idcard']
        user.user_company = request.POST['company']
        user.user_title = request.POST['title']
        user.user_addr = request.POST['addr']
        user.save()
        return HttpResponse(json.dumps({
            'statCode': 0
            }))
    except Exception as e:
        print(str(e))
        return render(request, "app/userInfo.html",{
            'id': user.user_name,
            'name': user.user_realName,
            'email':user.user_email,
            'addr':user.user_addr,
            'phone':user.user_phone,
            'idcard':user.user_idcard,
            'company':user.user_company,
            'title':user.user_title,
            })

@csrf_exempt
def adminInfo(request):
    # TODO
    return render(request, "app/adminInfo.html")


def uploadData(request):
    username = request.session['username']
    user = User.objects.get(user_name=username)
    user_id = user.user_id
    context = {}
    cursor = connection.cursor()
    sql = 'select data_name, data_info, timestamp, data_tag, data_download, data_status from BSCapp_data where BSCapp_data.user_id = %s ;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except :
        cursor.close()
        return context
    datas = []
    for i in range(len(content)):
        data = dict()
        data['name'] = content[i][0]
        data['info'] = content[i][1]
        data['timestamp'] = content[i][2]
        data['tag'] = content[i][3]
        data['download'] = content[i][4]
        data['status'] = content[i][5]
        datas.append(data)
    return render(request, "app/page-uploadData.html", {'datas': datas, 'id':username})
