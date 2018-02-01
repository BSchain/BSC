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
from time import time, localtime
import BSCapp.root_chain.coin as COIN

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
            'errormessage': 'Incorrect username or password',
            }))
    else:
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
        # print(user_id)
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
        return render(request, "app/page-userInfo.html",{
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
def buyableData(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id
    context = {}
    cursor = connection.cursor()
    sql = 'select data_id, user_id, data_name, data_info, timestamp, ' \
          'data_tag, data_status, data_md5, data_size, data_price ' \
          'from BSCapp_data where BSCapp_data.user_id != %s and BSCapp_data.data_status = 1;'
    # sql = 'select data_name, data_info, timestamp, data_tag, data_download, data_status, data_purchase, data_price \
    #             from BSCapp_data where BSCapp_data.data_status = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except :
        cursor.close()
        return context
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['data_id'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1]).user_name
        data['seller'] = seller
        data['name'] = content[i][2]
        data['info'] = content[i][3]
        data['timestamp'] = time_to_str(content[i][4])
        data['tag'] = content[i][5]
        data['md5'] = content[i][7]
        data['size'] = content[i][8]
        data['price'] = content[i][9]
        datas.append(data)
    return render(request, "app/page-buyableData.html", {'datas': datas, 'id':username})


@csrf_exempt
def adminDataInfo(request):
    username = request.session['username']
    try:
        now_admin = Admin.objects.get(admin_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    # username = request.session['username']
    # try:
    #     user = Admin.objects.get(admin_name=username)
    # except Exception:
    #     return render(request, "app/page-login.html")
    # try if it is triggered by a confirmation of a review
    try:
        now_admin_id = now_admin.admin_id
        now_data_id = request.POST['id']
        now_data_status = int(request.POST['op'])
        sql = 'update BSCapp_data set data_status = %s where data_id = %s;'
        cursor = connection.cursor()
        cursor.execute(sql, [now_data_status, now_data_id])
        cursor.close()

        now_data = Data.objects.get(data_id=now_data_id)
        seller_id = now_data.user_id
        now_action = ''
        if now_data_status == 1:
            now_action = 'review_pass'
        elif now_data_status == 2:
            now_action = 'review_reject'

        now_time = str(time())
        tx = TX.Transaction()
        tx.new_transaction(in_coins=[], out_coins=[], timestamp=now_time, action=now_action,
                           seller=seller_id, buyer='', data_uuid=now_data_id, credit=0.0, reviewer=now_admin_id)
        tx.save_transaction()

        try:
            review_history = Review.objects.get(data_id=now_data_id, reviewer_id=now_admin_id)
            review_history.review_status = now_data_status
            review_history.timestamp = now_time
            review_history.save()

            return HttpResponse(json.dumps({
                'statCode': 0,
            }))
        except Exception:
            Review(reviewer_id=now_admin_id, data_id=now_data_id, review_status=now_data_status, timestamp=now_time).save()
            return HttpResponse(json.dumps({
                'statCode': 0,
                }))
    except Exception:
        pass

    # else it is after logging in
    cursor = connection.cursor()
    sql = 'select data_id, user_id, data_name, data_info, timestamp, ' \
          'data_source, data_type, data_status, data_price from BSCapp_data;'
    try:
        cursor.execute(sql, [])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(str(e))
        cursor.close()
        return {}
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['dataid'] = content[i][0]
        seller = User.objects.get(user_id = content[i][1])
        data['seller'] = seller.user_realName
        data['name'] = content[i][2]
        data['info'] = content[i][3]
        data['timestamp'] = content[i][4]
        data['source'] = content[i][5]
        data['type'] = content[i][6]
        if content[i][7] == 0:
            data['status'] = '审核中'
        elif content[i][7] == 1:
            data['status'] = '审核通过'
        else:
            data['status'] = '审核不通过'
        data['price'] = content[i][8]
        datas.append(data)
    return render(request, "app/adminDataInfo.html", {'datas': datas})

@csrf_exempt
def upload(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")

    return render(request, "app/page-upload.html", {"username": username})


@csrf_exempt
def uploadData(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    if (request.method=="POST"):
        uploadFile = request.FILES.get("file", None)    #获得上传文件
        if not uploadFile:
            return render(request, "app/page-upload.html")
        # 打开特定的文件进行二进制的写操作，存在upload文件夹下，使用相对路径
        data_path = os.path.join("upload",uploadFile.name)
        destination = open(data_path,'wb+')
        for chunk in uploadFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        data_address = data_path + generate_uuid(uploadFile.name)
        data_name = request.POST["data_name"]   #获取数据信息
        data_id = generate_uuid(data_name)
        user_id = user.user_id
        data_info = request.POST['data_info']
        data_source = request.POST.getlist('data_source')[0]
        data_md5 = get_file_md5(data_path)
        data_size = uploadFile.size / 1024
        data_price = request.POST['data_price']

        data_type = request.POST.getlist('data_type')[0]
        data_tag = request.POST.getlist('data_tag')[0]

        Data(data_id=data_id, user_id=user_id, data_name=data_name,  data_info=data_info, timestamp= str(time()),
             data_source=data_source, data_type=data_type, data_tag=data_tag, data_status= 0, data_md5= data_md5,
             data_size=data_size, data_download=0, data_purchase=0, data_price=data_price, data_address = data_address,).save()

        now_time = str(time())
        # TODO: 1. generate new coin_id for the user_id
        # to keep the coin_id is unique, we use time() in generate_uuid
        new_coin_id = generate_uuid(data_id)
        default_coin_number = 1.0

        Coin(coin_id= new_coin_id, owner_id= user_id, is_spent=False,
             timestamp=now_time,coin_credit=default_coin_number).save()

        # TODO: 2. save transaction info to file
        out_coins = []
        coin = COIN.Coin()
        coin.new_coin(new_coin_id, default_coin_number, user_id)
        out_coins.append(coin.to_dict())
        tx = TX.Transaction()
        tx.new_transaction(in_coins=[], out_coins=out_coins, timestamp=now_time, action='upload',
                           seller=user_id, buyer='', data_uuid=data_id, credit=default_coin_number, reviewer='')
        tx.save_transaction()

        # TODO: 3. update the wallet of this user
        # because when user signup there must have a wallet for this user
        # that's why we just need to get the result out and sum those.
        wallet = Wallet.objects.get(user_id=user_id)
        # review_history = Review.objects.get(data_id=now_data_id, reviewer_id=now_admin_id)
        wallet.account = wallet.account + default_coin_number

        cursor = connection.cursor()
        sql = 'select coin_id , coin_credit from BSCapp_coin where BSCapp_coin.is_spent = FALSE and BSCapp.owner_id = %s'
        try:
            # check the user has those coin and those unspent coin total = wallet.account
            cursor.execute(sql, [user_id])
            content = cursor.fetchall()
            cursor.close()
            check_wallet_account = 0.0
            len_content = len(content)
            for i in len_content:
                check_wallet_account += content[i][1] # add all unspent coin together.
            if check_wallet_account != wallet.account:
                wallet.account = check_wallet_account
        except Exception:
            pass # something wrong in cursor, just pass, and use the waller.account

        wallet.save()
    user_id = user.user_id
    context = {}
    cursor = connection.cursor()
    sql = 'select data_name, data_info, timestamp, data_tag, data_download, data_status, data_purchase, data_price from BSCapp_data where BSCapp_data.user_id = %s ;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except :
        cursor.close()
        return context
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['name'] = content[i][0]
        data['info'] = content[i][1]
        data['timestamp'] = time_to_str(content[i][2])
        data['tag'] = content[i][3]
        data['download'] = content[i][4]
        # status = 0 审核中
        # status = 1 审核通过
        # status = 2 审核不通过
        # data['status'] = content[i][5]
        if content[i][5] == 0:
            data['status'] = '审核中'
        elif content[i][5] == 1:
            data['status'] = '审核通过'
        else:
            data['status'] = '审核不通过'
        data['purchase'] = content[i][6]
        data['price'] = content[i][7]
        datas.append(data)
    return render(request, "app/page-uploadData.html", {'datas': datas, 'id':username})

@csrf_exempt
def order(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id
    context = {}
    cursor = connection.cursor()
    sql = 'select BSCapp_data.data_id,BSCapp_data.user_id, BSCapp_data.data_name, BSCapp_data.data_info,BSCapp_data.data_source,' \
          'BSCapp_data.data_type, BSCapp_transaction.timestamp, BSCapp_transaction.price from BSCapp_data \
          ,BSCapp_transaction where BSCapp_data.data_id = BSCapp_transaction.data_id and BSCapp_transaction.buyer_id = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(str(e))
        cursor.close()
        return context
    orders = []
    len_content = len(content)
    for i in range(len_content):
        order = dict()
        order['dataid'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1])
        order['seller'] = seller.user_name
        order['name'] = content[i][2]
        order['info'] = content[i][3]
        order['source'] = content[i][4]
        order['type'] = content[i][5]
        order['timestamp'] = time_to_str(content[i][6])
        order['price'] = content[i][7]
        orders.append(order)
    return render(request, "app/page-order.html", {'orders': orders, 'id':username})

@csrf_exempt
def recharge(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id
    if (request.method=="POST"):
        amount = request.POST["amount"]
        now_time = str(time())
        # TODO: 1. generate new coin_id for the user_id
        # to keep the coin_id is unique, we use time() in generate_uuid
        new_coin_id = generate_uuid(user_id)
        default_coin_number = 1.0

        Coin(coin_id= new_coin_id, owner_id= user_id, is_spent=False,
             timestamp=now_time,coin_credit=default_coin_number).save()

        # TODO: 2. modify wallet of the user_id
        cursor = connection.cursor()
        sql = 'update BSCapp_wallet set BSCapp_wallet.account = BSCapp_wallet.account + %s where BSCapp_wallet.user_id = %s;'
        try:
            cursor.execute(sql, [amount, user_id])
            cursor.close()
        except Exception as e:
            print(str(e))
            cursor.close()
            return context


    return render(request, "app/page-recharge.html", {'id':username})
