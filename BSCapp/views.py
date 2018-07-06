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


# Create your views here.

@csrf_exempt
def Index(request):

    try:
        now_block_height = request.POST['height']
        now_block_dict = get_block_by_index_json(now_block_height)
        return HttpResponse(json.dumps({
            'statCode': 0,
            'message': 'block height is ' + str(now_block_height),
            'block': json.dumps(now_block_dict),
        }))
    except Exception as e:
        # print(e)
        pass
    try:
        Block_sort_name_and_type = request.session['Block_sort_name_and_type']
        if Block_sort_name_and_type == "":
            request.session['Block_sort_name_and_type'] = "timestamp&DESC"
    except Exception as e:
        # print(e)
        request.session['Block_sort_name_and_type'] = "timestamp&DESC"
    try:
        Block_sort_name_and_type = request.session['Block_sort_name_and_type']
        result = Block_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]

        new_sort_name = request.POST['sort_name']

        if (new_sort_name != 'height' and new_sort_name != 'timestamp' and new_sort_name != 'block_size' and
                new_sort_name != 'tx_number' and new_sort_name != 'block_hash'):
            new_sort_name = 'timestamp'

        if new_sort_name == default_sort_name:
            new_sort_type = 'DESC' if default_sort_type == 'ASC' else 'ASC'  # the same just ~
        else:
            new_sort_type = 'DESC'  # default = DESC

        request.session['Block_sort_name_and_type'] = new_sort_name + '&' + new_sort_type
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        # print(e)
        pass

    Block_sort_name_and_type = request.session['Block_sort_name_and_type']
    result = Block_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    myData_sort_list = ['height', 'timestamp', 'block_size', 'tx_number', 'block_hash']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, myData_sort_list)

    table_name = 'BSCapp_block'
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)

    blocks, len_content = chainData_sql(request, sort_sql)
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        if search_field == '':
            paged_blocks = pagingData(request, blocks)
        else:
            paged_blocks = pagingData(request, blocks, each_num=len_content)
    except Exception as e:
        # print(e)
        paged_blocks = pagingData(request, blocks)

    request.session['username'] = ""
    request.session['isAdmin'] = False
    request.session['Admin_sort_name_and_type'] = ""
    request.session['Buy_sort_name_and_type'] = ""
    request.session['Order_sort_name_and_type'] = ""
    request.session['Notice_sort_name_and_type'] = ""
    request.session['MyData_sort_name_and_type'] = ""

    return render(request, "app/page-index.html",
                  {'blocks': paged_blocks,
                   'sort_class': sort_class})


    # return render(request, "app/page-index.html")

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
            request.session['Block_sort_name_and_type'] = "timestamp&DESC"
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
        request.session['Block_sort_name_and_type'] = "timestamp&DESC"

        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            'isAdmin': 0,
            }))

@csrf_exempt

def FindPwd(request):
    try:
        now_user_name = request.POST['username']
        now_user_email = request.POST['email']
        try:
            user = User.objects.get(user_name=now_user_name)
        except Exception as e:

            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '用户名或邮箱有误，请重新输入!',
            }))
        if user.user_email != now_user_email:
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '用户名或邮箱有误，请重新输入!',
            }))

        # print(now_user_name, now_user_email)
        # 生成随机数链接 保存至数据库，记录当前时间
        # 发送邮件通知，将生成的url发送给用户
        # 用户修改密码发送通知
        # 用户修改密码生成transaction文件

        # send email to now_user
        secretKey = generate_uuid(now_user_name + now_user_email )
        sendResult = sendResetPwdEmail(receiver= now_user_email, secretKey = secretKey)

        if sendResult == True: # send success!!!

            # update or insert the Reset table
            try:
                user_reset = Reset.objects.get(user_name = now_user_name)
                user_reset.secretKey = secretKey # update the secret key
                user_reset.last_reset_time = time() # update the last forgot password time
                user_reset.save()
            except Exception as e:
                # print(e) # the first time to reset password
                Reset(user_name= now_user_name, secretKey= secretKey, last_reset_time= time()).save()

            # send notices to user
            now_user = User.objects.get(user_name=now_user_name)
            notice_info = '{} 在 {} 发起重置密码请求'.format(now_user_name, time_to_str(time()))
            Notice(notice_id=generate_uuid(now_user.user_id), sender_id='系统',
                   receiver_id=now_user.user_id,
                   notice_type=4, notice_info=notice_info, if_check=False, timestamp=time(), if_delete=False).save()

            # generate now transaction file
            tx = TX.Transaction()
            tx.new_transaction(in_coins=[], out_coins=[],
                               timestamp=str(datetime.datetime.utcnow().timestamp()), action='reset_pwd',
                               seller=now_user.user_id, buyer='', data_uuid='', credit=0, reviewer='')
            tx.save_transaction()

            return HttpResponse(json.dumps({
                'statCode': 0,
                'message': '重置密码邮件发送成功!!!',
            }))

        else:
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '邮件发送失败，请稍后重试!!!',
            }))
    except Exception as e:
        # print(e)
        return render(request, "app/page-findPwd.html")

@csrf_exempt
def ResetPwd(request):
    now_secretKey = request.get_full_path()[1:-1]
    # print(now_secretKey)
    user_name = ''
    try:
        user_reset = Reset.objects.get(secretKey=now_secretKey)
        user_name = user_reset.user_name
        # print(user_name)
        now_time = (float)(time())
        last_modify_time = (float)(user_reset.last_reset_time)
        #TODO: add empireTime to config
        empireTime = 30 * 60
        if now_time - last_modify_time > empireTime: # find password
            return render(request, "app/page-findPwd.html")

    except Exception as e:
        # print(e) # something wrong with this secret key
        return render(request, "app/page-findPwd.html")

    try:
        user_password = request.POST['password']
        user_repassword= request.POST['repassword']
        if (user_password != user_repassword):
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '两次输入密码不一致,请重新输入!',
            }))
        # set to empire
        user_reset.last_reset_time = 0
        user_reset.save()

        User.objects.filter(user_name=user_name).update(user_pwd = user_password)
        return HttpResponse(json.dumps({
            'statCode': 0,
            'message': '密码修改成功，请重新登录!',
        }))
    except Exception as e:
        # print(e)
        pass
    return render(request, "app/page-resetPwd.html", {'username':user_name})

@csrf_exempt
def ModifyPwd(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception as e:
        return render(request, "app/page-login.html")

    try:
        old_pwd = request.POST['old_password']
        new_pwd = request.POST['new_password']
        new_repwd = request.POST['new_repassword']

        if old_pwd != user.user_pwd:
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '密码输入错误,请重新输入!',
            }))
        if new_pwd != new_repwd:
            return HttpResponse(json.dumps({
                'statCode': -2,
                'message': '密码不一致，请重新输入!',
            }))
        if old_pwd == new_pwd:
            return HttpResponse(json.dumps({
                'statCode': -3,
                'message': '密码修改前后一致，请重新输入!',
            }))
        # update the password
        user.user_pwd = new_pwd
        user.save()
        tx = TX.Transaction()
        tx.new_transaction(in_coins=[], out_coins=[],
                           timestamp=str(datetime.datetime.utcnow().timestamp()), action='modify_pwd',
                           seller=user.user_id, buyer='', data_uuid='', credit=0, reviewer='')
        tx.save_transaction()

        notice_info = '{} 在 {} 修改密码成功'.format(username, time_to_str(time()))
        # send notify to user
        Notice(notice_id= generate_uuid(user.user_id), sender_id='系统', receiver_id=user.user_id,
           notice_type=4, notice_info=notice_info, if_check=False,
           timestamp=time(), if_delete=False).save()

        try:
            user_modify = Modify.objects.get(user_name=username)
            user_name = user_modify.user_name
            # print(user_name)
            now_time = (float)(time())
            last_modify_time = (float)(user_modify.last_modify_time)
            # TODO: add empireTime to config
            empireTime = 30 * 60
            if now_time - last_modify_time > empireTime:  # find password
                return HttpResponse(json.dumps({
                    'statCode': -1,
                    'message': '30分钟内仅允许一次密码修改操作,请稍后重试!',
                }))

        except Exception as e:
            print(e)
            Modify(user_name=user.user_name, last_modify_time=time()).save()
            return HttpResponse(json.dumps({
                'statCode': 0,
                'message': '密码修改成功,请重新登录!',
            }))

        user_modify.last_modify_time = 0
        user_modify.save()

        return HttpResponse(json.dumps({
            'statCode': 0,
            'message': '密码修改成功,请重新登录!',
        }))

    except Exception as e:
        return render(request, "app/page-modifyPwd.html",{"username": username})


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
            'errormessage': '用户名已注册,请重新输入!',
            }))
    except Exception:
        pass
    #username cannot be signed up before
    try:
        u = User.objects.get(user_name=user_name)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '用户名已注册,请重新输入!',
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
                'errormessage': '邮箱已注册,请重新输入!',
                }))
        else:
            #the password and password input again have to be the same
            if (user_pwd!=user_repwd):
                return HttpResponse(json.dumps({
                    'statCode': -3,
                    'errormessage': '两次输入密码不一致,请重新输入!',
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
        account = Wallet.objects.get(user_id=user.user_id).account
        account = round(account,3)
        #get the number of upload data
        upload_data_num = len(GetUploadData(user.user_id))
        #get the number of purchase data
        purchase_data_num = len(GetPurchaseData(user.user_id))

        # #get the recharge record
        # recharges = rechargeData_sql(user.user_id)
        # paged_recharges = pagingData(request, recharges)
        tx_logs = txLog_sql(user.user_id)
        paged_tx_logs = pagingData(request, tx_logs)

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
            # 'recharges':paged_recharges,
            'tx_logs': paged_tx_logs,
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
        now_data_id = request.POST['data_id']
        now_op = request.POST['op']
        try:
            seller_id = ScienceData.objects.get(data_id=now_data_id).user_id  # get seller
        except Exception as e:
            # print(e)
            pass
        if now_op == 'download':
            try:
                now_data = ScienceData.objects.get(data_id=now_data_id)
                Purchase.objects.get(user_id=buyer_id, data_id=now_data_id)
                try:
                    now_data_file_address = Data.objects.get(data_id = now_data_id).data_address
                    file_path = os.getcwd() +"/BSCapp"+now_data_file_address[2:]
                    if(os.path.exists(file_path) == False):
                        return HttpResponse(json.dumps({
                            'statCode': -1,
                            'message': '当前数据已失效，请联系管理员!'
                        }))
                except Exception as e:
                    # print(e)
                    return HttpResponse(json.dumps({
                        'statCode': -1,
                        'message': '当前数据已失效!'
                    }))
                # get last download time
                try:
                    old_last_download_time = Transaction.objects.get(buyer_id=buyer_id,
                                                                     data_id=now_data_id).last_download_time
                    if old_last_download_time == '':  # the first time to download data
                        now_time = str(datetime.datetime.utcnow().timestamp())
                        cursor = connection.cursor()
                        sql = 'update BSCapp_transaction set BSCapp_transaction.last_download_time = %s where buyer_id = %s and data_id = %s'
                        cursor.execute(sql, [now_time, buyer_id, now_data_id])
                        cursor.close()
                    else:
                        limit_download_time = 300  # same data only download once in 5 minutes
                        old_last_download_time = (float)(old_last_download_time)
                        now_time = (float)(str(datetime.datetime.utcnow().timestamp()))
                        left_time = now_time - old_last_download_time
                        if left_time < limit_download_time:
                            return HttpResponse(json.dumps({
                                'statCode': -1,
                                'message': '同一数据5分钟内仅可下载一次! 剩余等待时间:' + str((int)(limit_download_time - left_time)) + '秒'
                            }))
                        else:  # between the 300 seconds
                            now_time = str(datetime.datetime.utcnow().timestamp())
                            cursor = connection.cursor()
                            sql = 'update BSCapp_transaction set BSCapp_transaction.last_download_time = %s where buyer_id = %s and data_id = %s'
                            cursor.execute(sql, [now_time, buyer_id, now_data_id])
                            cursor.close()
                except Exception as e:
                    # print(e)
                    pass
                # add action: download to file
                tx = TX.Transaction()
                tx.new_transaction(in_coins=[], out_coins=[],
                                   timestamp=str(datetime.datetime.utcnow().timestamp()), action='download',
                                   seller=seller_id, buyer=buyer_id, data_uuid=now_data_id, credit=0, reviewer='')
                tx.save_transaction()

                cursor = connection.cursor()
                sql = 'update BSCapp_data set BSCapp_data.data_download = BSCapp_data.data_download + 1 where data_id = %s'
                cursor.execute(sql, [now_data_id])
                cursor.close()

                return HttpResponse(json.dumps({
                    'statCode': 0,
                    'name':now_data.data_name,
                    'address':now_data.data_address,
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
    except Exception as e:
        # print(e)
        pass

    try:
        Buy_sort_name_and_type = request.session['Buy_sort_name_and_type']
        result = Buy_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        if(new_sort_name != 'data_name' and new_sort_name != 'data_info' and new_sort_name != 'timestamp' and
                new_sort_name != 'first_title' and new_sort_name != 'second_title' and
                new_sort_name != 'data_type' and new_sort_name!='data_size'):

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
        # print(e)
        pass

    Buy_sort_name_and_type = request.session['Buy_sort_name_and_type']
    result = Buy_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    table_name = 'BSCapp_sciencedata'
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)

    datas, len_content = buyData_sql(request, buyer_id, sort_sql)
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        if search_field == '':
            paged_datas = pagingData(request, datas)
        else:
            paged_datas = pagingData(request, datas, each_num=len_content)
    except Exception as e:
        paged_datas = pagingData(request, datas)

    notices, unread_notices, unread_number = get_notices(request, buyer_id)

    buyData_sort_list = ['data_name', 'data_info', 'timestamp', 'first_title', 'second_title', 'data_type', 'data_size']
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
        now_op = request.POST['op']
        now_data_status = 0
        if now_op == 'reject':
            now_data_status = 2
        elif now_op == 'pass':
            now_data_status = 1
        sql = 'update BSCapp_sciencedata set data_status = %s where data_id = %s;'
        cursor = connection.cursor()
        cursor.execute(sql, [now_data_status, now_data_id])
        cursor.close()

        now_data = ScienceData.objects.get(data_id=now_data_id)
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
        try: # can change
            review_history = Review.objects.get(data_id=now_data_id, reviewer_id=now_admin_id)
            if review_history.review_status == now_data_status:
                return HttpResponse(json.dumps({
                    'statCode': 0,
                }))
            review_history.review_status = now_data_status
            review_history.timestamp = now_time
            review_history.save()
        except Exception as e:
            # print(e)
            # the first time to review data
            Review(reviewer_id=now_admin_id, data_id=now_data_id, review_status=now_data_status, timestamp=now_time).save()

        # generate notice for a successful recharge
        cursor = connection.cursor()
        notice_insert = 'insert into BSCapp_notice \
                                (notice_id, sender_id, receiver_id, notice_type, notice_info, if_check, timestamp, if_delete) \
                                values \
                                (%s, %s, %s, %s, %s, 0, %s, False);'
        sender_id = now_admin_id
        notice_id = generate_uuid(sender_id)
        receiver_id = now_data.user_id
        timestamp = datetime.datetime.utcnow().timestamp()
        if now_action == 'review_pass':
            notice_type = 1
            notice_info = '{} 在 {} 审核 {} 通过'.format(now_admin.admin_name, time_to_str(timestamp),
                                                    now_data.data_name)
        else:
            notice_type = 2
            notice_info = '{} 在 {} 审核 {} 不通过'.format(now_admin.admin_name, time_to_str(timestamp),
                                                     now_data.data_name)
        cursor.execute(notice_insert, [notice_id, sender_id, receiver_id, notice_type,
                                       notice_info, timestamp])
        cursor.close()

        return HttpResponse(json.dumps({
            'statCode': 0,
        }))

    except Exception as e:
        # print(e)
        pass

    try:
        Admin_sort_name_and_type = request.session['Admin_sort_name_and_type']
        result = Admin_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        if (new_sort_name != 'data_name' and new_sort_name != 'data_info' and new_sort_name != 'timestamp' and
                new_sort_name != 'data_source' and new_sort_name != 'first_title' and new_sort_name != 'second_title' and
                new_sort_name != 'data_type' and new_sort_name!= 'data_size' and new_sort_name != 'data_status'):
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
        # print(e)
        pass
    Admin_sort_name_and_type = request.session['Admin_sort_name_and_type']
    result = Admin_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    if default_sort_name == 'user_id':
        table_name = 'BSCapp_user'
    else:
        table_name = 'BSCapp_sciencedata'


    try:
        func = request.POST['func']
        if func == 'reviewAllPass':
            data_all_pass_status = 1
            data_all_reject_status = 2
            data_all_waiting_status = 0
            # get all reject data
            cursor = connection.cursor()
            sql = 'select data_id from BSCapp_sciencedata where data_status = %s or data_status = %s;'
            cursor.execute(sql, [data_all_reject_status, data_all_waiting_status])
            cursor.close()
            content = cursor.fetchall()
            # calculate the data number
            len_all_pass_data = len(content)

            for i in range(len_all_pass_data):
                # print('data id', content[i][0])
                now_data_id = content[i][0]
                now_data = ScienceData.objects.get(data_id=now_data_id)
                now_data.data_status = data_all_pass_status
                now_data.save()
                seller_id = now_data.user_id
                now_action = 'review_pass'
                now_time = str(datetime.datetime.utcnow().timestamp())

                # generate transaction files
                tx = TX.Transaction()
                tx.new_transaction(in_coins=[], out_coins=[], timestamp=now_time, action=now_action,
                                   seller=seller_id, buyer='', data_uuid=now_data_id, credit=0.0, reviewer=now_admin_id)
                tx.save_transaction()

                # insert the review into history and save a notice
                try:  # can change
                    review_history = Review.objects.get(data_id=now_data_id, reviewer_id=now_admin_id)
                    review_history.review_status = data_all_pass_status
                    review_history.timestamp = now_time
                    review_history.save()
                except Exception as e:
                    # print(e)
                    # the first time to review data
                    Review(reviewer_id=now_admin_id, data_id=now_data_id, review_status=data_all_pass_status,
                           timestamp=now_time).save()

                # generate notice for a successful recharge
                cursor = connection.cursor()
                notice_insert = 'insert into BSCapp_notice \
                                                (notice_id, sender_id, receiver_id, notice_type, notice_info, if_check, timestamp, if_delete) \
                                                values \
                                                (%s, %s, %s, %s, %s, 0, %s, 0);'
                sender_id = now_admin_id
                notice_id = generate_uuid(sender_id)
                receiver_id = now_data.user_id
                timestamp = datetime.datetime.utcnow().timestamp()

                notice_type = 1
                notice_info = '{} 在 {} 审核 {} 通过'.format(now_admin.admin_name, time_to_str(timestamp),
                                                            now_data.data_name)
                cursor.execute(notice_insert, [notice_id, sender_id, receiver_id, notice_type,
                                               notice_info, timestamp])
                cursor.close()

            return HttpResponse(json.dumps({
                'statCode': 0,
                'message': '审核完成!'
            }))

    except Exception as e:
        # print(e)
        pass
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)
    datas = adminData_sql(request,sort_sql)
    paged_datas = pagingData(request, datas)
    adminData_sort_list = ['data_name', 'data_info', 'timestamp', 'data_source', 'data_type', 'data_price',
                           'data_status', 'data_purchase', 'data_download', 'data_score', 'comment_number', 'data_size']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, adminData_sort_list)

    return render(request, "app/page-adminDataInfo.html", {'id':username, 'datas': paged_datas, 'sort_class': sort_class})

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
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '未上传数据，请上传数据!'
            }))
            # return render(request, "app/page-upload.html")
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
        data_type = request.POST['data_type']
        data_source = request.POST['data_source']
        first_title = request.POST['first_title']
        second_title = request.POST['second_title']
        data_size = uploadFile.size / (1024 * 1024)

        if data_name == '' :
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '数据名未填写，请填写数据名！'
            }))
        if data_info == '':
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '数据简介未填写，请填写数据简介！'
            }))
        if data_source == '':
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '数据来源未填写，请填写数据来源！'
            }))
        if second_title == '' or second_title == '科研资源':
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '所属科技资源未填写，请填写科技资源！'
            }))

        ScienceData(data_id=data_id, user_id=user_id, timestamp= str(datetime.datetime.utcnow().timestamp()),
             data_name=data_name, data_source=data_source, data_info=data_info, data_type=data_type,
             first_title = first_title,second_title = second_title,
             data_address = data_address, data_status= 0, data_size=data_size).save()

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

    myData_sort_list = ['data_name', 'data_info', 'timestamp', 'first_title', 'second_title',
                        'data_type', 'data_status', 'data_size']
    try:
        MyData_sort_name_and_type = request.session['MyData_sort_name_and_type']
        result = MyData_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        if (new_sort_name != 'data_name' and new_sort_name != 'data_info' and new_sort_name != 'timestamp' and
                new_sort_name != 'first_title' and new_sort_name != 'second_title' and
                new_sort_name != 'data_type' and new_sort_name!='data_status' and new_sort_name!='data_size'):
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
        # print(e)
        pass
    MyData_sort_name_and_type = request.session['MyData_sort_name_and_type']
    result = MyData_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]


    sort_class = generate_sort_class(default_sort_name, default_sort_type, myData_sort_list)

    table_name = 'BSCapp_sciencedata'
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)
    # print(sort_sql)

    datas, len_content = uploadData_sql(request, user_id, sort_sql)
    try:
        search_field = request.POST["searcBase"]
        search_field = request.POST["searchField"]
        if search_field == '':
            paged_datas = pagingData(request, datas)
        else:
            paged_datas = pagingData(request, datas,each_num=len_content)
    except Exception as e:
        paged_datas = pagingData(request, datas)

    notices, unread_notices, unread_number = get_notices(request, user_id)

    return render(request, "app/page-myData.html", {'datas': paged_datas,
                                                    'id':username,
                                                    'sort_class':sort_class,
                                                    'unread_number':unread_number,
                                                    'unread_notices':unread_notices})

@csrf_exempt
def Order(request):
    try:
        username = request.session['username']
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id
    # get the data score Done!
    # add the data score to the transaction table
    # update the data_avg_score in data table
    # update the comment_number in data table
    try:
        self_data_score = (int)(request.POST['data_score'])
        rating_data_id = request.POST['rating_data_id']
        #
        # print('self_data_score',self_data_score)
        # print('rating_data_id', rating_data_id)
        # print('user_id', user_id)
        # insert self_score into transaction table
        try:
            cursor = connection.cursor()
            sql = 'update BSCapp_transaction ' \
                  'set BSCapp_transaction.data_score = %s where buyer_id = %s and data_id = %s'
            cursor.execute(sql, [self_data_score, user_id, rating_data_id])
            cursor.close()

            # get old data_avg_score and comment_number
            rating_data = Data.objects.get(data_id= rating_data_id)
            old_data_avg_score = rating_data.data_score
            old_comment_number = rating_data.comment_number

            # calculate the new score
            new_data_avg_score = (float)((old_data_avg_score * old_comment_number + self_data_score) / (old_comment_number + 1))
            new_comment_number = old_comment_number + 1


            # update the data_avg_score and comment_number in data table
            try:
                cursor = connection.cursor()
                sql = 'update BSCapp_data ' \
                      'set BSCapp_data.data_score = %s, BSCapp_data.comment_number = %s ' \
                      'where data_id = %s'
                cursor.execute(sql, [new_data_avg_score, new_comment_number, rating_data_id])
                cursor.close()
            except Exception as e:
                print(str(e))
                # rechange to no score state
                default_score = 0.0
                cursor = connection.cursor()
                sql = 'update BSCapp_transaction ' \
                      'set BSCapp_transaction.data_score = %s where buyer_id = %s and data_id = %s'
                cursor.execute(sql, [default_score, user_id, rating_data_id])
                cursor.close()

                return HttpResponse(json.dumps({
                    'statCode': -1,
                    'message': '评价失败！'
                }))

            return HttpResponse(json.dumps({
                'statCode': 0,
                'message': '评价成功！'
            }))
        except Exception as e:
            # print(str(e))
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '评价失败！'
            }))
    except Exception as e:
        # print(e)
        pass
    try:
        # add download action in Order page
        now_data_id = request.POST['data_id']
        now_op = request.POST['op']
        seller_id = Data.objects.get(data_id=now_data_id).user_id  # get seller
        if now_op == 'download':
            try:
                Purchase.objects.get(user_id=user_id, data_id=now_data_id)
                now_data = Data.objects.get(data_id = now_data_id)
                try:

                    now_data_file_address = Data.objects.get(data_id = now_data_id).data_address
                    file_path = os.getcwd() +"/BSCapp"+now_data_file_address[2:]
                    if(os.path.exists(file_path) == False):
                        return HttpResponse(json.dumps({
                            'statCode': -1,
                            'message': '当前数据已失效，请联系管理员!'
                        }))
                except Exception as e:
                    # print(e)
                    return HttpResponse(json.dumps({
                        'statCode': -1,
                        'message': '当前数据已失效!'
                    }))
                # get last download time
                try:
                    old_last_download_time = Transaction.objects.get(buyer_id = user_id, data_id = now_data_id).last_download_time
                    if old_last_download_time == '': # the first time to download data
                        now_time = str(datetime.datetime.utcnow().timestamp())
                        cursor = connection.cursor()
                        sql = 'update BSCapp_transaction set BSCapp_transaction.last_download_time = %s where buyer_id = %s and data_id = %s'
                        cursor.execute(sql, [now_time, user_id, now_data_id])
                        cursor.close()
                    else:
                        limit_download_time = 300 # same data only download once in 5 minutes
                        old_last_download_time = (float)(old_last_download_time)
                        now_time = (float)(str(datetime.datetime.utcnow().timestamp()))
                        left_time = now_time - old_last_download_time
                        if  left_time < limit_download_time:
                            return HttpResponse(json.dumps({
                                'statCode': -1,
                                'message': '同一数据5分钟内仅可下载一次! 剩余等待时间:'+str((int)(limit_download_time - left_time))+'秒'
                            }))
                        else: # between the 300 seconds
                            now_time = str(datetime.datetime.utcnow().timestamp())
                            cursor = connection.cursor()
                            sql = 'update BSCapp_transaction set BSCapp_transaction.last_download_time = %s where buyer_id = %s and data_id = %s'
                            cursor.execute(sql, [now_time, user_id, now_data_id])
                            cursor.close()
                except Exception as e:
                    # print(e)
                    pass
                # add action: download to file
                tx = TX.Transaction()
                tx.new_transaction(in_coins=[], out_coins=[],
                                   timestamp=str(datetime.datetime.utcnow().timestamp()), action='download',
                                   seller=seller_id, buyer=user_id, data_uuid=now_data_id, credit=0, reviewer='')
                tx.save_transaction()

                # change the download numebr
                cursor = connection.cursor()
                sql = 'update BSCapp_data set BSCapp_data.data_download = BSCapp_data.data_download + 1 where data_id = %s'
                cursor.execute(sql, [now_data_id])
                cursor.close()

                return HttpResponse(json.dumps({
                    'statCode': 0,
                    'address': now_data.data_address,
                    'name': now_data.data_name,
                    'message': '已购买此数据,可以下载!'
                }))
            except:
                return HttpResponse(json.dumps({
                    'statCode': -1,
                    'message': '未购买此数据,无法下载!'
                }))
        # insert new purchase_log for buyer
    except Exception as e:
        # print(e)
        pass

    try:
        Buy_sort_name_and_type = request.session['Order_sort_name_and_type']
        result = Buy_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        # check name in data table
        if (new_sort_name!='user_id' and new_sort_name != 'data_name' and new_sort_name != 'data_info' and
                new_sort_name != 'timestamp' and new_sort_name != 'data_source' and new_sort_name != 'data_type'and
                new_sort_name != 'price' and new_sort_name!='data_score' and new_sort_name!='comment_number'):
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
        # print(e)
        pass
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
    paged_orders = pagingData(request, orders)
    notices, unread_notices, unread_number = get_notices(request, user_id)

    order_sort_list = ['data_name', 'data_info', 'timestamp', 'data_source', 'data_type', 'price', 'data_score', 'comment_number']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, order_sort_list)

    return render(request, "app/page-order.html", {'orders': paged_orders,
                                                   'id': username,
                                                   'sort_class':sort_class,
                                                   'unread_number':unread_number,
                                                   'unread_notices':unread_notices})


@csrf_exempt
def DataStatistics(request):
    try:
        username = request.session['username']
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id
    # get the data score Done!
    # add the data score to the transaction table
    # update the data_avg_score in data table
    # update the comment_number in data table
    try:
        self_data_score = (int)(request.POST['data_score'])
        rating_data_id = request.POST['rating_data_id']
        #
        # print('self_data_score',self_data_score)
        # print('rating_data_id', rating_data_id)
        # print('user_id', user_id)
        # insert self_score into transaction table
        try:
            cursor = connection.cursor()
            sql = 'update BSCapp_transaction ' \
                  'set BSCapp_transaction.data_score = %s where buyer_id = %s and data_id = %s'
            cursor.execute(sql, [self_data_score, user_id, rating_data_id])
            cursor.close()

            # get old data_avg_score and comment_number
            rating_data = Data.objects.get(data_id= rating_data_id)
            old_data_avg_score = rating_data.data_score
            old_comment_number = rating_data.comment_number

            # calculate the new score
            new_data_avg_score = (float)((old_data_avg_score * old_comment_number + self_data_score) / (old_comment_number + 1))
            new_comment_number = old_comment_number + 1


            # update the data_avg_score and comment_number in data table
            try:
                cursor = connection.cursor()
                sql = 'update BSCapp_data ' \
                      'set BSCapp_data.data_score = %s, BSCapp_data.comment_number = %s ' \
                      'where data_id = %s'
                cursor.execute(sql, [new_data_avg_score, new_comment_number, rating_data_id])
                cursor.close()
            except Exception as e:
                print(str(e))
                # rechange to no score state
                default_score = 0.0
                cursor = connection.cursor()
                sql = 'update BSCapp_transaction ' \
                      'set BSCapp_transaction.data_score = %s where buyer_id = %s and data_id = %s'
                cursor.execute(sql, [default_score, user_id, rating_data_id])
                cursor.close()

                return HttpResponse(json.dumps({
                    'statCode': -1,
                    'message': '评价失败！'
                }))

            return HttpResponse(json.dumps({
                'statCode': 0,
                'message': '评价成功！'
            }))
        except Exception as e:
            # print(str(e))
            return HttpResponse(json.dumps({
                'statCode': -1,
                'message': '评价失败！'
            }))
    except Exception as e:
        # print(e)
        pass
    try:
        # add download action in Order page
        now_data_id = request.POST['data_id']
        now_op = request.POST['op']
        seller_id = Data.objects.get(data_id=now_data_id).user_id  # get seller
        if now_op == 'download':
            try:
                Purchase.objects.get(user_id=user_id, data_id=now_data_id)
                now_data = Data.objects.get(data_id = now_data_id)
                try:

                    now_data_file_address = Data.objects.get(data_id = now_data_id).data_address
                    file_path = os.getcwd() +"/BSCapp"+now_data_file_address[2:]
                    if(os.path.exists(file_path) == False):
                        return HttpResponse(json.dumps({
                            'statCode': -1,
                            'message': '当前数据已失效，请联系管理员!'
                        }))
                except Exception as e:
                    # print(e)
                    return HttpResponse(json.dumps({
                        'statCode': -1,
                        'message': '当前数据已失效!'
                    }))
                # get last download time
                try:
                    old_last_download_time = Transaction.objects.get(buyer_id = user_id, data_id = now_data_id).last_download_time
                    if old_last_download_time == '': # the first time to download data
                        now_time = str(datetime.datetime.utcnow().timestamp())
                        cursor = connection.cursor()
                        sql = 'update BSCapp_transaction set BSCapp_transaction.last_download_time = %s where buyer_id = %s and data_id = %s'
                        cursor.execute(sql, [now_time, user_id, now_data_id])
                        cursor.close()
                    else:
                        limit_download_time = 300 # same data only download once in 5 minutes
                        old_last_download_time = (float)(old_last_download_time)
                        now_time = (float)(str(datetime.datetime.utcnow().timestamp()))
                        left_time = now_time - old_last_download_time
                        if  left_time < limit_download_time:
                            return HttpResponse(json.dumps({
                                'statCode': -1,
                                'message': '同一数据5分钟内仅可下载一次! 剩余等待时间:'+str((int)(limit_download_time - left_time))+'秒'
                            }))
                        else: # between the 300 seconds
                            now_time = str(datetime.datetime.utcnow().timestamp())
                            cursor = connection.cursor()
                            sql = 'update BSCapp_transaction set BSCapp_transaction.last_download_time = %s where buyer_id = %s and data_id = %s'
                            cursor.execute(sql, [now_time, user_id, now_data_id])
                            cursor.close()
                except Exception as e:
                    # print(e)
                    pass
                # add action: download to file
                tx = TX.Transaction()
                tx.new_transaction(in_coins=[], out_coins=[],
                                   timestamp=str(datetime.datetime.utcnow().timestamp()), action='download',
                                   seller=seller_id, buyer=user_id, data_uuid=now_data_id, credit=0, reviewer='')
                tx.save_transaction()

                # change the download numebr
                cursor = connection.cursor()
                sql = 'update BSCapp_data set BSCapp_data.data_download = BSCapp_data.data_download + 1 where data_id = %s'
                cursor.execute(sql, [now_data_id])
                cursor.close()

                return HttpResponse(json.dumps({
                    'statCode': 0,
                    'address': now_data.data_address,
                    'name': now_data.data_name,
                    'message': '已购买此数据,可以下载!'
                }))
            except:
                return HttpResponse(json.dumps({
                    'statCode': -1,
                    'message': '未购买此数据,无法下载!'
                }))
        # insert new purchase_log for buyer
    except Exception as e:
        # print(e)
        pass

    try:
        Buy_sort_name_and_type = request.session['Order_sort_name_and_type']
        result = Buy_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        # check name in data table
        if (new_sort_name!='user_id' and new_sort_name != 'data_name' and new_sort_name != 'data_info' and
                new_sort_name != 'timestamp' and new_sort_name != 'data_source' and new_sort_name != 'data_type'and
                new_sort_name != 'price' and new_sort_name!='data_score' and new_sort_name!='comment_number'):
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
        # print(e)
        pass
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
    paged_orders = pagingData(request, orders)
    notices, unread_notices, unread_number = get_notices(request, user_id)

    order_sort_list = ['data_name', 'data_info', 'timestamp', 'data_source', 'data_type', 'price', 'data_score', 'comment_number']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, order_sort_list)

    return render(request, "app/page-dataStatistics.html", {'orders': paged_orders,
                                                   'id': username,
                                                   'sort_class':sort_class,
                                                   'unread_number':unread_number,
                                                   'unread_notices':unread_notices})


# @csrf_exempt
# def Recharge(request):
#     username = request.session['username']
#     try:
#         user = User.objects.get(user_name=username)
#     except Exception:
#         return render(request, "app/page-login.html")
#     user_id = user.user_id
#
#     try:
#         account = request.POST["account"]
#         reaccount = request.POST["reaccount"]
#         amount = request.POST["amount"]
#
#         # print('account',account)
#         # print('reaccount', reaccount)
#         # print('amount','amount')
#
#         if account != reaccount:
#             return HttpResponse(json.dumps({
#                 'statCode': -1,
#                 'message': '账户不同,请重新输入！'
#             }))
#         try:
#             check_user = User.objects.get(user_name=account)
#             account_user_id =  check_user.user_id
#         except Exception as e:
#             return HttpResponse(json.dumps({
#                 'statCode': -1,
#                 'message': '账户:'+account+' 不存在，请重新输入!'
#             }))
#         try:
#             amount = (float)(amount)
#             if amount <=0 :
#                 return HttpResponse(json.dumps({
#                     'statCode': -1,
#                     'message': '充值金额应大于0，请重新输入!'
#                 }))
#         except Exception as e:
#             return HttpResponse(json.dumps({
#                 'statCode': -1,
#                 'message': '充值金额有误，请重新输入!'
#             }))
#         now_time = str(datetime.datetime.utcnow().timestamp())
#         #1. generate new coin_id for the user_id
#         # to keep the coin_id is unique, we use datetime.datetime.utcnow().timestamp() in generate_uuid amount means the recharge money
#
#         new_coin_id = generate_uuid(account_user_id)
#
#         Coin(coin_id=new_coin_id, owner_id=account_user_id, is_spent=False,
#              timestamp=now_time,coin_credit=amount).save()
#
#         buyer_coin = COIN.Coin()
#         buyer_coin.new_coin(coin_uuid=new_coin_id, number_coin=amount, owner=account_user_id)
#         out_coins = []
#         out_coins.append(buyer_coin.to_dict())
#
#         tx = TX.Transaction()
#         tx.new_transaction(in_coins=[], out_coins=out_coins, timestamp=datetime.datetime.utcnow().timestamp(), action='recharge',
#                            seller=user_id, buyer='', data_uuid='', credit=amount, reviewer='')
#         tx.save_transaction()
#
#         #get the wallet account before recharge
#         before_account = Wallet.objects.get(user_id=account_user_id).account
#         # before_account = GetAccount(user_id)
#
#         #2. modify wallet of the user_id
#         cursor = connection.cursor()
#         sql = 'update BSCapp_wallet set BSCapp_wallet.account = %s + %s where BSCapp_wallet.user_id = %s;'
#         try:
#             cursor.execute(sql, [before_account, amount, account_user_id])
#             cursor.close()
#         except Exception as e:
#             cursor.close()
#         #get the wallet account after recharge
#         after_account = Wallet.objects.get(user_id=account_user_id).account
#         # after_account = GetAccount(user_id)
#
#         #3. add the recharge record into the recharge tables
#         recharge_id = generate_uuid(account_user_id)
#         cursor = connection.cursor()
#         sql = 'insert into BSCapp_recharge(recharge_id, user_id, timestamp, credits, before_account, after_account, coin_id) values (%s,%s,%s,%s,%s,%s,%s);'
#         try:
#             timestamp = datetime.datetime.utcnow().timestamp()
#             cursor.execute(sql, [recharge_id, account_user_id, timestamp, amount, before_account, after_account, new_coin_id])
#             cursor.close()
#         except Exception as e:
#             cursor.close()
#         # 4. generate notice for a successful recharge
#         cursor = connection.cursor()
#         notice_insert = 'insert into BSCapp_notice \
#             (notice_id, sender_id, receiver_id, notice_type, notice_info, if_check, timestamp) \
#             values \
#             (%s, %s, %s, %s, %s, 0, %s)'
#         sender_id = user_id
#         notice_id = generate_uuid(sender_id)
#         receiver_id = account_user_id
#         notice_type = 3
#         timestamp = datetime.datetime.utcnow().timestamp()
#         notice_info = '{} 在 {} 为账户 {} 充值成功, 充值金额为 {}'.format(username, time_to_str(timestamp), account, amount)
#         cursor.execute(notice_insert, [notice_id, sender_id, receiver_id, notice_type,
#                                        notice_info, timestamp])
#         cursor.close()
#         return HttpResponse(json.dumps({
#             'statCode': 0,
#             'message': '充值成功!'
#         }))
#     except Exception as e:
#         # print(e)
#         pass
#     notices, unread_notices, unread_number = get_notices(request, user_id)
#
#     return render(request, "app/page-recharge.html",
#                   {'id':username,
#                    'unread_number':unread_number,
#                    'unread_notices':unread_notices})

@csrf_exempt
def Notify(request):
    username = request.session['username']
    try:
        user = User.objects.get(user_name=username)
    except Exception:
        return render(request, "app/page-login.html")
    user_id = user.user_id

    try:
        now_func = request.POST['func']
        # print('now_func',now_func)
        if now_func == 'deleteAll':
            try:
                sql = 'update BSCapp_notice set if_delete = True where receiver_id = %s and if_check = True and if_delete = False'
                cursor = connection.cursor()
                cursor.execute(sql, [user_id])
                cursor.close()
                return HttpResponse(json.dumps({
                    'statCode': 0,
                    'message': '删除成功!'
                }))
            except Exception as e:
                # print(e)
                pass
        elif now_func == 'readAll':
            try:
                sql = 'update BSCapp_notice set if_check = True where receiver_id = %s and if_check = False and if_delete = False;'
                cursor = connection.cursor()
                cursor.execute(sql, [user_id])
                cursor.close()
                return HttpResponse(json.dumps({
                    'statCode': 0,
                    'message': '标记成功!'
                }))
            except Exception as e:
                # print(e)
                pass
    except Exception as e:
        # print(e)
        pass
    try:
        now_notice_id = request.POST['id']
        now_op = request.POST['op']
        notice = Notice.objects.get(notice_id=now_notice_id)
        now_if_check = False
        if now_op == 'delete':
            try:
                sql = 'update BSCapp_notice set if_delete = True where notice_id = %s;'
                cursor = connection.cursor()
                cursor.execute(sql, [now_notice_id])
                cursor.close()
            except Exception as e:
                # print(e)
                pass

        elif now_op == 'read':
            now_if_check = True
        elif now_op == 'unread':
            now_if_check = False

        if notice.if_check == now_if_check:
            return HttpResponse(json.dumps({
                'statCode': 0,
            }))

        try:
            sql = 'update BSCapp_notice set if_check = %s where notice_id = %s and if_delete = False;'
            cursor = connection.cursor()
            cursor.execute(sql, [now_if_check,now_notice_id])
            cursor.close()
        except Exception as e:
            # print(e)
            pass

        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        # print(e)
        pass

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
        # print(e)
        pass

    notices, unread_notices, unread_number = get_notices(request, user_id)

    Notice_sort_name_and_type = request.session['Notice_sort_name_and_type']
    result = Notice_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]
    notify_sort_list = ['timestamp', 'notice_info', 'if_check']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, notify_sort_list)

    paged_notices = pagingData(request, notices)

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
    notices, unread_notices, unread_number = get_notices(request, user_id)
    try:
        now_block_height = request.POST['height']
        now_block_dict = get_block_by_index_json(now_block_height)
        content = {}
        cursor = connection.cursor()
        sql = 'select tx_number,timestamp from BSCapp_block where BSCapp_block.height = %s;'
        try:
            cursor.execute(sql, [now_block_height])
            content = cursor.fetchall()
            cursor.close()
        except Exception as e:
            cursor.close()
        one_block_txNumber = content[0][0]
        one_block_timestamp = time_to_str(content[0][1])


        return HttpResponse(json.dumps({
            'statCode': 0,
            'message': 'block height is '+str(now_block_height),
            'block': json.dumps(now_block_dict),
            'txNumber': one_block_txNumber,
            'timestamp': one_block_timestamp,
        }))
    except Exception as e:
        pass

    # sort_sql = generate_sort_sql(table_name = 'BSCapp_block', sort_name = 'height', sort_type = 'DESC')

    try:
        Block_sort_name_and_type = request.session['Block_sort_name_and_type']
        result = Block_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        if (new_sort_name != 'height' and new_sort_name != 'timestamp' and new_sort_name != 'block_size' and
                new_sort_name != 'tx_number' and new_sort_name != 'block_hash'):
            new_sort_name = 'timestamp'

        if new_sort_name == default_sort_name:
            new_sort_type = 'DESC' if default_sort_type == 'ASC' else 'ASC'  # the same just ~
        else:
            new_sort_type = 'DESC'  # default = DESC

        request.session['Block_sort_name_and_type'] = new_sort_name + '&' + new_sort_type
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        # print(e)
        pass

    Block_sort_name_and_type = request.session['Block_sort_name_and_type']
    result = Block_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    myData_sort_list = ['height', 'timestamp', 'block_size', 'tx_number', 'block_hash']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, myData_sort_list)

    table_name = 'BSCapp_block'
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)

    blocks, len_content = chainData_sql(request, sort_sql)
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        if search_field == '':
            paged_blocks = pagingData(request, blocks)
        else:
            paged_blocks = pagingData(request, blocks, each_num=len_content)
    except Exception as e:
        # print(e)
        paged_blocks = pagingData(request, blocks)

    return render(request, "app/page-chainInfo.html",
                      {'id': username,
                       'blocks': paged_blocks,
                       'sort_class': sort_class,
                       'unread_number': unread_number,
                       'unread_notices': unread_notices})

@csrf_exempt
def AdminChainInfo(request):
    username = request.session['username']
    user = Admin.objects.get(admin_name=username)
    try:
        now_block_height = request.POST['height']
        now_block_dict = get_block_by_index_json(now_block_height)
        return HttpResponse(json.dumps({
            'statCode': 0,
            'message': 'block height is '+str(now_block_height),
            'block': json.dumps(now_block_dict),
        }))
    except Exception as e:
        pass

    try:
        Block_sort_name_and_type = request.session['Block_sort_name_and_type']
        result = Block_sort_name_and_type.split('&')
        default_sort_name = result[0]
        default_sort_type = result[1]
        new_sort_name = request.POST['sort_name']
        if (new_sort_name != 'height' and new_sort_name != 'timestamp' and new_sort_name != 'block_size' and
                new_sort_name != 'tx_number' and new_sort_name != 'block_hash'):
            new_sort_name = 'timestamp'

        if new_sort_name == default_sort_name:
            new_sort_type = 'DESC' if default_sort_type == 'ASC' else 'ASC'  # the same just ~
        else:
            new_sort_type = 'DESC'  # default = DESC

        request.session['Block_sort_name_and_type'] = new_sort_name + '&' + new_sort_type
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except Exception as e:
        # print(e)
        pass

    Block_sort_name_and_type = request.session['Block_sort_name_and_type']
    result = Block_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    myData_sort_list = ['height', 'timestamp', 'block_size', 'tx_number', 'block_hash']
    sort_class = generate_sort_class(default_sort_name, default_sort_type, myData_sort_list)

    table_name = 'BSCapp_block'
    # default sort using session
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)

    blocks,len_content = chainData_sql(request, sort_sql)
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        if search_field == '':
            paged_blocks = pagingData(request, blocks)
        else:
            paged_blocks = pagingData(request, blocks, each_num=len_content)
    except Exception as e:
        # print(e)
        paged_blocks = pagingData(request, blocks)

    return render(request, "app/page-adminChainInfo.html",
                      {'id': username,
                       'blocks': paged_blocks,
                       'sort_class': sort_class})