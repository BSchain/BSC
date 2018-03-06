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
from BSCapp.function import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@csrf_exempt
def Index(request):
    request.session['username'] = ""
    request.session['isAdmin'] = False
    request.session['Admin_sort_name_and_type'] = ""
    request.session['Buy_sort_name_and_type'] = ""
    request.session['Order_sort_name_and_type'] = ""
    request.session['Notice_sort_name_and_type'] = ""
    request.session['MyData_sort_name_and_type'] = ""

    return render(request, "app/page-index.html")

@csrf_exempt
def Login(request):
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
            tx.new_transaction(in_coins=[], out_coins=[],timestamp=datetime.datetime.utcnow().timestamp(), action='login',
                               seller=a.admin_id, buyer='',data_uuid='',credit=0.0, reviewer='')
            tx.save_transaction()

            request.session['username'] = username
            request.session['isAdmin'] = True
            # add sort session for admin
            request.session['Admin_sort_name_and_type'] = 'timestamp&DESC'

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
        tx.new_transaction(in_coins=[], out_coins=[],timestamp=datetime.datetime.utcnow().timestamp(), action='login',
                           seller=u.user_id, buyer='',data_uuid='',credit=0.0, reviewer='')
        tx.save_transaction()

        request.session['username'] = username
        request.session['isAdmin'] = False
        # add sort session for user
        request.session['Buy_sort_name_and_type'] = 'timestamp&DESC'
        request.session['Order_sort_name_and_type'] = 'timestamp&DESC'
        request.session['Upload_sort_name_and_type'] = 'timestamp&DESC'
        request.session['Notice_sort_name_and_type'] = "timestamp&DESC"
        request.session['MyData_sort_name_and_type'] = "timestamp&DESC"

        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            'isAdmin': 0,
            }))

@csrf_exempt
def Signup(request):
    # get the info of user sign up
    try:
        user_name = request.POST['username']
        user_pwd = request.POST['password']
        user_repwd = request.POST['repassword']
        user_email = request.POST['email']
        user_id = generate_uuid(user_name)
    except Exception as e:
        return render(request, "app/page-signUp.html")
    # client cannot overwrite admin users
    try:
        u = Admin.objects.get(admin_name=user_name)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '用户名已注册',
            }))
    except Exception:
        pass
    #username cannot be signed up before
    try:
        u = User.objects.get(user_name=user_name)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '用户名已注册',
            }))
    except Exception as e:
        #email cannot be signed up before
        sql = 'select user_name from BSCapp_user where BSCapp_user.user_email=%s';
        content = {}
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [user_email])
            content = cursor.fetchall()
            cursor.close()
        except:
            cursor.close()
        if len(content)>0:
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': '邮箱已注册',
                }))
        else:
            #the password and password input again have to be the same
            if (user_pwd!=user_repwd):
                return HttpResponse(json.dumps({
                    'statCode': -3,
                    'errormessage': '两次输入密码不一致',
                    }))
            User(user_id=user_id, user_name=user_name,
                user_pwd=user_pwd, user_email=user_email).save()
            Wallet(user_id=user_id, account = 0.0).save()
            return HttpResponse(json.dumps({
                'statCode': 0,
                'username': user_name,
                }))

@csrf_exempt
def UserInfo(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception as e:
        return render(request, "app/page-login.html")
    try:
        user.user_realName = request.POST['realname']
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
        #get the account of user and accurate to the second decimal place
        account = round(GetAccount(user.user_id),2)
        #get the number of upload data
        upload_data_num = len(GetUploadData(user.user_id))
        #get the number of purchase data
        purchase_data_num = len(GetPurchaseData(user.user_id))
        #get the recharge record
        recharges = rechargeData_sql(user.user_id)
        paged_recharges = pagingData(request, recharges, each_num = 10)

        notices, unread_notices, unread_number = get_notices(request, user.user_id)

        return render(request, "app/page-userInfo.html",{
            'id': user.user_name,
            'name': user.user_realName,
            'email':user.user_email,
            'addr':user.user_addr,
            'phone':user.user_phone,
            'idcard':user.user_idcard,
            'company':user.user_company,
            'title':user.user_title,
            'account':account,
            'upload_data_num':upload_data_num,
            'purchase_data_num':purchase_data_num,
            'recharges':paged_recharges,
            'unread_number': unread_number,
            'unread_notices': unread_notices
            })

@csrf_exempt
def BuyableData(request):
    username = request.session['username']

    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")

    buyer_id = user.user_id  # get buyer

    try:
        # print(request.POST['data_id'])
        now_data_id = request.POST['data_id']
        now_op = request.POST['op']
        seller_id = Data.objects.get(data_id=now_data_id).user_id  # get seller
        if now_op == 'download':
            try:
                Purchase.objects.get(user_id=buyer_id, data_id=now_data_id)
                # add action: download to file
                tx = TX.Transaction()
                tx.new_transaction(in_coins=[], out_coins=[],
                                   timestamp=str(datetime.datetime.utcnow().timestamp()), action='download',
                                   seller=seller_id, buyer=buyer_id, data_uuid=now_data_id, credit=0, reviewer='')
                tx.save_transaction()
                return HttpResponse(json.dumps({
                    'statCode': 0,
                    'message': '已购买此数据,可以下载!'
                }))
            except:
                return HttpResponse(json.dumps({
                    'statCode': -1,
                    'message': '未购买此数据,无法下载!'
                }))
        # insert new purchase_log for buyer
        try:
            Purchase.objects.get(user_id=buyer_id, data_id=now_data_id)
            return HttpResponse(json.dumps({  # 到这一步说明已经购买过数据
                'statCode': -3,
                'message': '已经购买此数据，请勿重复购买！'
            }))
        except:
            pass # 数据还未购买,则可以进行购买操作

        # whether this user can buy data
        user_balance = Wallet.objects.get(user_id=buyer_id).account
        now_data_price = Data.objects.get(data_id=now_data_id).data_price
        if user_balance < now_data_price:
            return HttpResponse(json.dumps({
                'statCode': -2,
                'message': '余额不足!'
            }))

        # get user unspent coins
        try:
            cursor = connection.cursor()
            sql = 'select coin_id, coin_credit from BSCapp_coin ' \
              'where BSCapp_coin.owner_id = %s and BSCapp_coin.is_spent = False'
            cursor.execute(sql,[buyer_id])
            content = cursor.fetchall()

            # get user in_coins
            in_coins = []
            len_content = len(content); coin_numbers = 0; coin_credicts = 0
            for i in range(len_content):
                if coin_credicts >= now_data_price:
                    break
                coin_numbers+=1
                buyer_coin = COIN.Coin()
                buyer_coin.new_coin(coin_uuid=content[i][0],number_coin=content[i][1],owner=buyer_id)
                coin_credicts += content[i][1]
                in_coins.append(buyer_coin.to_dict())

            # generate out_coins
            out_coins = []
            left_credit = coin_credicts - now_data_price
            if left_credit > 0:
                buyer_out_coin = COIN.Coin()
                buyer_out_coin.new_coin(coin_uuid=generate_uuid(buyer_id),number_coin=left_credit, owner=buyer_id)
                out_coins.append(buyer_out_coin.to_dict())

            seller_out_coin = COIN.Coin()
            seller_out_coin.new_coin(coin_uuid=generate_uuid(seller_id), number_coin=now_data_price, owner=seller_id)
            out_coins.append(seller_out_coin.to_dict())

            # insert one purchase log into table
            Purchase(user_id=buyer_id,data_id=now_data_id).save()

            # generate new transactions for action: buy
            tx = TX.Transaction()
            tx.new_transaction(in_coins=in_coins,out_coins=out_coins, timestamp=str(datetime.datetime.utcnow().timestamp()), action='buy',
                               seller=seller_id, buyer=buyer_id, data_uuid= now_data_id, credit= now_data_price, reviewer='')
            tx.save_transaction()

            # update the coin table is_spent = True
            cursor = connection.cursor()
            for i in range(coin_numbers):
                item_coin_id = in_coins[i]['coin_uuid']
                sql = 'update BSCapp_coin set is_spent = True where coin_id = %s'
                cursor.execute(sql,[item_coin_id])

            # insert new coin for buyer and seller
            if left_credit > 0:
                Coin(coin_id = buyer_out_coin.to_dict()['coin_uuid'], owner_id=buyer_id,
                     is_spent=False, timestamp=str(datetime.datetime.utcnow().timestamp()), coin_credit=left_credit).save()
            Coin(coin_id=seller_out_coin.to_dict()['coin_uuid'], owner_id=seller_id,
                     is_spent=False, timestamp=str(datetime.datetime.utcnow().timestamp()), coin_credit=now_data_price).save()

            # update the wallet of buyer and seller
            sql = 'update BSCapp_wallet set  BSCapp_wallet.account = BSCapp_wallet.account + %s where user_id = %s'
            cursor.execute(sql, [0 - now_data_price, buyer_id])
            cursor.execute(sql, [now_data_price, seller_id])
            sql = 'update BSCapp_data set BSCapp_data.data_download = data_download + 1 where data_id = %s'
            cursor.execute(sql, [now_data_id])
            cursor.close()

            # generate a new transaction for mysql
            Transaction(transaction_id=generate_uuid(buyer_id+seller_id), buyer_id=buyer_id, seller_id= seller_id,
                        data_id=now_data_id, timestamp=str(datetime.datetime.utcnow().timestamp()), price=now_data_price).save()
            return HttpResponse(json.dumps({
                'statCode': 0,
                'message': '购买成功!'
            }))
        except:
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '系统错误!'
            }))
    except:
        pass

    try:
        Buy_sort_name_and_type = request.session['Buy_sort_name_and_type']
        result = Buy_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        if(new_sort_name!='user_id' and new_sort_name != 'data_name' and new_sort_name != 'data_info' and
                new_sort_name != 'timestamp' and new_sort_name != 'data_tag' and new_sort_name != 'data_md5' and
                new_sort_name != 'data_size' and new_sort_name!='data_price'):

            new_sort_name = 'timestamp'

        if new_sort_name == default_sort_name:
            new_sort_type = 'DESC' if default_sort_type == 'ASC' else 'ASC' # the same just ~
        else:
            new_sort_type = 'DESC' # default = DESC

        request.session['Buy_sort_name_and_type'] = new_sort_name + '&' + new_sort_type

        return HttpResponse(json.dumps({
                'statCode': 0,
            }))
    except Exception as e:
        print(e)

    Buy_sort_name_and_type = request.session['Buy_sort_name_and_type']
    result = Buy_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    table_name = 'BSCapp_data'
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)

    datas = buyData_sql(request, buyer_id, sort_sql)

    paged_datas = pagingData(request, datas, each_num= 10)
    notices, unread_notices, unread_number = get_notices(request, buyer_id)

    buyData_sort_list = ['data_name', 'data_info', 'timestamp', 'data_tag', 'data_md5', 'data_size', 'data_price']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, buyData_sort_list)

    return render(request, "app/page-buyableData.html", {'datas': paged_datas,
                                                         'id':username,
                                                         'sort_class': sort_class,
                                                         'unread_number':unread_number,
                                                         'unread_notices':unread_notices})

@csrf_exempt
def AdminDataInfo(request):
    username = request.session['username']
    try:
        now_admin = Admin.objects.get(admin_name=username)
    except Exception:
        return render(request, "app/page-login.html")
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

        now_time = str(datetime.datetime.utcnow().timestamp())
        tx = TX.Transaction()
        tx.new_transaction(in_coins=[], out_coins=[], timestamp=now_time, action=now_action,
                           seller=seller_id, buyer='', data_uuid=now_data_id, credit=0.0, reviewer=now_admin_id)
        tx.save_transaction()
        # insert the review into history and save a notice
        try:
            review_history = Review.objects.get(data_id=now_data_id, reviewer_id=now_admin_id)
            review_history.review_status = now_data_status
            review_history.timestamp = now_time
            review_history.save()
            # generate notice for a successful recharge
            cursor = connection.cursor()
            notice_insert = 'insert into BSCapp_notice \
                (notice_id, sender_id, receiver_id, notice_type, notice_info, if_check, timestamp) \
                values \
                (%s, %s, %s, %s, %s, 0, %s);'
            sender_id = now_admin_id
            notice_id = generate_uuid(sender_id)
            receiver_id = now_data.user_id
            timestamp = datetime.datetime.utcnow().timestamp()
            if now_action == 'review_pass':
                notice_type = 1
                notice_info = '{} 在 {} 审核 {} 通过'.format(now_admin.admin_name, time_to_str(timestamp), now_data.data_name)
            else:
                notice_type = 2
                notice_info = '{} 在 {} 审核 {} 不通过'.format(now_admin.admin_name, time_to_str(timestamp), now_data.data_name)
            cursor.execute(notice_insert, [notice_id, sender_id, receiver_id, notice_type,
                                           notice_info, timestamp])
            cursor.close()
            return HttpResponse(json.dumps({
                'statCode': 0,
            }))
        except Exception as e:
            print(e)
            cursor.close()
            Review(reviewer_id=now_admin_id, data_id=now_data_id, review_status=now_data_status, timestamp=now_time).save()
            return HttpResponse(json.dumps({
                'statCode': 0,
                }))

    except Exception:
        pass

    try:
        Admin_sort_name_and_type = request.session['Admin_sort_name_and_type']
        result = Admin_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        if (new_sort_name != 'data_name' and new_sort_name != 'data_info' and new_sort_name != 'timestamp' and
                new_sort_name != 'data_source' and new_sort_name != 'data_type' and new_sort_name != 'data_price' and
                new_sort_name != 'data_status'):
            new_sort_name = 'timestamp'

        if new_sort_name == default_sort_name:
            new_sort_type = 'DESC' if default_sort_type == 'ASC' else 'ASC'  # the same just ~
        else:
            new_sort_type = 'DESC'  # default = DESC

        request.session['Admin_sort_name_and_type'] = new_sort_name + '&' + new_sort_type

        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        print(e)

    Admin_sort_name_and_type = request.session['Admin_sort_name_and_type']
    result = Admin_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    if default_sort_name == 'user_id':
        table_name = 'BSCapp_user'
    else:
        table_name = 'BSCapp_data'

    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)
    datas = adminData_sql(request,sort_sql)
    paged_datas = pagingData(request, datas, each_num=10)
    adminData_sort_list = ['data_name', 'data_info', 'timestamp', 'data_source', 'data_type', 'data_price', 'data_status']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, adminData_sort_list)

    return render(request, "app/page-adminDataInfo.html", {'datas': paged_datas, 'sort_class': sort_class})

@csrf_exempt
def Upload(request):
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
        data_path = os.path.join("BSCapp/static/upload",uploadFile.name)
        destination = open(data_path,'wb+')
        for chunk in uploadFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        data_address = os.path.join("../static/upload",uploadFile.name)
        data_name = request.POST["data_name"]   #获取数据信息
        data_id = generate_uuid(data_name)
        user_id = user.user_id
        data_info = request.POST['data_info']
        data_source = request.POST.getlist('data_source')[0]
        data_md5 = get_file_md5(data_path)
        data_size = uploadFile.size / (1024 * 1024)
        data_price = request.POST['data_price']

        data_type = request.POST.getlist('data_type')[0]
        data_tag = request.POST.getlist('data_tag')[0]

        #find out whether there is same data uploaded before
        content = {}
        cursor = connection.cursor()
        sql = 'select data_id from BSCapp_data where BSCapp_data.data_md5 = %s'
        try:
            # get the data where md5 is the same as upload data
            cursor.execute(sql, [data_md5])
            content = cursor.fetchall()
        except Exception:
            pass # something wrong in cursor, just pass, and use the wallet.account
        #if there are some data with the same md5, then return error statCode
        if (len(content)>0):
            conflict_data_id = content[0][0] # get the data_id
            confilct_data = Data.objects.get(data_id = conflict_data_id)

            conflict_data_name = confilct_data.data_name # get the data name
            owner_id = confilct_data.user_id # get the data owner_id
            sender_id = 'system'
            owner_notice_id = generate_uuid(sender_id)
            timestamp = time()
            owner_notice_type = 4
            owner_notice_info = '{} 在 {} 上传冲突数据 {}.'.format(username, time_to_str(timestamp), conflict_data_name)

            # send notice to data owner
            Notice(notice_id=owner_notice_id, sender_id=sender_id, receiver_id=owner_id,
                   notice_type=owner_notice_type, notice_info=owner_notice_info, if_check=False,
                   timestamp=timestamp).save()

            conflict_notice_type = 4
            conflict_notice_info = '{} 在 {} 上传冲突数据 {}, 该数据md5为 {}.'.format(username, time_to_str(timestamp), conflict_data_name, confilct_data.data_md5)

            conflict_notice_id = generate_uuid(sender_id)
            # send notict to data uploader
            Notice(notice_id = conflict_notice_id, sender_id = sender_id, receiver_id= user.user_id,
                   notice_type= conflict_notice_type, notice_info= conflict_notice_info, if_check=False, timestamp=timestamp).save()

            return HttpResponse(json.dumps({
                'statCode': -1,
            }))

        Data(data_id=data_id, user_id=user_id, data_name=data_name,  data_info=data_info, timestamp= str(datetime.datetime.utcnow().timestamp()),
             data_source=data_source, data_type=data_type, data_tag=data_tag, data_status= 0, data_md5= data_md5,
             data_size=data_size, data_download=0, data_purchase=0, data_price=data_price, data_address = data_address,).save()

        now_time = str(datetime.datetime.utcnow().timestamp())
        # TODO: 1. generate new coin_id for the user_id
        # to keep the coin_id is unique, we use datetime.datetime.utcnow().timestamp() in generate_uuid
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
            pass # something wrong in cursor, just pass, and use the wallet.account
        wallet.save()
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    notices, unread_notices, unread_number = get_notices(request, user.user_id)
    return render(request, "app/page-upload.html", {"username": username,
                                                    'unread_number':unread_number,
                                                    'unread_notices':unread_notices})

@csrf_exempt
def MyData(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")

    user_id = user.user_id

    try:
        MyData_sort_name_and_type = request.session['MyData_sort_name_and_type']
        result = MyData_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        if (new_sort_name != 'data_name' and new_sort_name != 'data_info' and new_sort_name != 'timestamp' and
                new_sort_name != 'data_tag' and new_sort_name != 'data_status' and new_sort_name != 'data_purchase' and
                new_sort_name!='data_download' and new_sort_name != 'data_price'):
            new_sort_name = 'timestamp'

        if new_sort_name == default_sort_name:
            new_sort_type = 'DESC' if default_sort_type == 'ASC' else 'ASC'  # the same just ~
        else:
            new_sort_type = 'DESC'  # default = DESC

        request.session['MyData_sort_name_and_type'] = new_sort_name + '&' + new_sort_type
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        print(e)

    MyData_sort_name_and_type = request.session['MyData_sort_name_and_type']
    result = MyData_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    myData_sort_list = ['data_name', 'data_info', 'timestamp', 'data_tag', 'data_status', 'data_purchase', 'data_download', 'data_price']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, myData_sort_list)

    table_name = 'BSCapp_data'
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)

    datas = uploadData_sql(request, user_id, sort_sql)

    paged_datas = pagingData(request, datas, each_num=10)

    notices, unread_notices, unread_number = get_notices(request, user_id)

    return render(request, "app/page-myData.html", {'datas': paged_datas,
                                                    'id':username,
                                                    'sort_class':sort_class,
                                                    'unread_number':unread_number,
                                                    'unread_notices':unread_notices})

@csrf_exempt
def Order(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id
    try:
        # add download action in Order page
        now_data_id = request.POST['data_id']
        now_op = request.POST['op']
        seller_id = Data.objects.get(data_id=now_data_id).user_id  # get seller

        if now_op == 'download':
            try:
                Purchase.objects.get(user_id=user_id, data_id=now_data_id)
                # add action: download to file
                tx = TX.Transaction()
                tx.new_transaction(in_coins=[], out_coins=[],
                                   timestamp=str(datetime.datetime.utcnow().timestamp()), action='download',
                                   seller=seller_id, buyer=user_id, data_uuid=now_data_id, credit=0, reviewer='')
                tx.save_transaction()
                return HttpResponse(json.dumps({
                    'statCode': 0,
                    'message': '已购买此数据,可以下载!'
                }))
            except:
                return HttpResponse(json.dumps({
                    'statCode': -1,
                    'message': '未购买此数据,无法下载!'
                }))
        # insert new purchase_log for buyer
    except Exception as e:
        print(e)
    try:
        Buy_sort_name_and_type = request.session['Order_sort_name_and_type']
        result = Buy_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        # check name in data table
        if (new_sort_name!='user_id' and new_sort_name != 'data_name' and new_sort_name != 'data_info' and
                new_sort_name != 'timestamp' and new_sort_name != 'data_source' and new_sort_name != 'data_type'and new_sort_name != 'price'):
            new_sort_name = 'timestamp'

        if new_sort_name == default_sort_name:
            new_sort_type = 'DESC' if default_sort_type == 'ASC' else 'ASC'  # the same just ~
        else:
            new_sort_type = 'DESC'  # default = DESC

        request.session['Order_sort_name_and_type'] = new_sort_name + '&' + new_sort_type

        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        print(e)

    Order_sort_name_and_type = request.session['Order_sort_name_and_type']
    result = Order_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]
    table_name = 'BSCapp_data'
    if default_sort_name == 'price' or default_sort_name == 'timestamp':
        table_name = 'BSCapp_transaction'
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)
    orders = orderData_sql(request, user_id, sort_sql)
    paged_orders = pagingData(request, orders, each_num=10)
    notices, unread_notices, unread_number = get_notices(request, user_id)

    order_sort_list = ['data_name', 'data_info', 'timestamp', 'data_source', 'data_type', 'price']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, order_sort_list)

    return render(request, "app/page-order.html", {'orders': paged_orders,
                                                   'id': username,
                                                   'sort_class':sort_class,
                                                   'unread_number':unread_number,
                                                   'unread_notices':unread_notices})

@csrf_exempt
def Recharge(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id
    if (request.method=="POST"):
        amount = request.POST["amount"]
        now_time = str(datetime.datetime.utcnow().timestamp())
        #1. generate new coin_id for the user_id
        # to keep the coin_id is unique, we use datetime.datetime.utcnow().timestamp() in generate_uuid amount means the recharge money
        new_coin_id = generate_uuid(user_id)

        Coin(coin_id=new_coin_id, owner_id=user_id, is_spent=False,
             timestamp=now_time,coin_credit=amount).save()

        #get the wallet account before recharge
        before_account = GetAccount(user_id)

        #2. modify wallet of the user_id
        cursor = connection.cursor()
        sql = 'update BSCapp_wallet set BSCapp_wallet.account = %s + %s where BSCapp_wallet.user_id = %s;'
        try:
            cursor.execute(sql, [before_account, amount, user_id])
            cursor.close()
        except Exception as e:
            cursor.close()
        #get the wallet account after recharge
        after_account = GetAccount(user_id)

        #3. add the recharge record into the recharge tables
        recharge_id = generate_uuid(user_id)
        cursor = connection.cursor()
        sql = 'insert into BSCapp_recharge(recharge_id, user_id, timestamp, credits, before_account, after_account, coin_id) values (%s,%s,%s,%s,%s,%s,%s);'
        try:
            timestamp = datetime.datetime.utcnow().timestamp()
            cursor.execute(sql, [recharge_id, user_id, timestamp, amount, before_account, after_account, new_coin_id])
            cursor.close()
        except Exception as e:
            cursor.close()
        # 4. generate notice for a successful recharge
        cursor = connection.cursor()
        notice_insert = 'insert into BSCapp_notice \
            (notice_id, sender_id, receiver_id, notice_type, notice_info, if_check, timestamp) \
            values \
            (%s, %s, %s, %s, %s, 0, %s)'
        sender_id = 'system'
        notice_id = generate_uuid(sender_id)
        receiver_id = user_id
        notice_type = 3
        timestamp = datetime.datetime.utcnow().timestamp()
        notice_info = '{} 在 {} 充值成功'.format(username, time_to_str(timestamp))
        cursor.execute(notice_insert, [notice_id, sender_id, receiver_id, notice_type,
                                       notice_info, timestamp])
    notices, unread_notices, unread_number = get_notices(request, user_id)

    return render(request, "app/page-recharge.html",
                  {'id':username,
                   'unread_number':unread_number,
                   'unread_notices':unread_notices})

@csrf_exempt
def Notify(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id
    try:
        now_notice_id = request.POST['id']
        now_op = request.POST['op']
        notice = Notice.objects.get(notice_id=now_notice_id)
        if notice.if_check != now_op:
            sql = 'update BSCapp_notice set if_check = %s where notice_id = %s;'
            cursor = connection.cursor()
            cursor.execute(sql, [now_op,now_notice_id])
            cursor.close()
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        print(e)

    try:
        Notice_sort_name_and_type = request.session['Notice_sort_name_and_type']
        result = Notice_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        # check name in data table
        if (new_sort_name!='timestamp' and new_sort_name != 'notice_info' and new_sort_name != 'if_check'):
            new_sort_name = 'timestamp'

        if new_sort_name == default_sort_name:
            new_sort_type = 'DESC' if default_sort_type == 'ASC' else 'ASC'  # the same just ~
        else:
            new_sort_type = 'DESC'  # default = DESC

        request.session['Notice_sort_name_and_type'] = new_sort_name + '&' + new_sort_type


        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        print(e)

    notices, unread_notices, unread_number = get_notices(request, user_id)

    Notice_sort_name_and_type = request.session['Notice_sort_name_and_type']
    result = Notice_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]
    notify_sort_list = ['timestamp', 'notice_info', 'if_check']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, notify_sort_list)

    paged_notices = pagingData(request, notices, each_num=10)

    return render(request, "app/page-notify.html",
                  {'notices': paged_notices,
                   'id': username,
                   'sort_class': sort_class,
                   'unread_number':unread_number,
                   'unread_notices':unread_notices
                   })
@csrf_exempt
def ChainInfo(request):
    username = request.session['username']
    user = User.objects.get(user_name=username)
    user_id = user.user_id
    try:
        now_block_height = request.POST['height']
        now_op = request.POST['op']
    except Exception:
        pass

    notices, unread_notices, unread_number = get_notices(request, user_id)
    blocks = chainData_sql()
    paged_blocks = pagingData(request, blocks, each_num=10)

    return render(request, "app/page-chainInfo.html",
                  {'id': username,
                   'blocks': paged_blocks,
                   'unread_number': unread_number,
                   'unread_notices': unread_notices})

