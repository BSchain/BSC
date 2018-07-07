# -*- coding: utf-8 -*-
# @Time    : 01/02/2018 4:25 PM
# @Author  : 伊甸一点
# @FileName: function.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from django.db import connection
from BSCapp.root_chain.utils import *
from BSCapp.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class JuncheePaginator(Paginator):
    def __init__(self, object_list, per_page, range_num=4, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num

    def page(self, number):
        self.page_num = (int)(number)
        return super(JuncheePaginator, self).page(number)

    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1
        if self.num_pages <= num_count:
            return range(1, self.num_pages + 1)
        num_list = []
        num_list.append(self.page_num)
        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)

            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)
        num_list.sort()
        return num_list

    page_range_ext = property(_page_range_ext)

def generate_sort_sql(table_name, sort_name, sort_type):
    sort_sql = 'order by ' + table_name + '.' + sort_name+' '+sort_type+';'
    return sort_sql

def buyData_sql(request, buyer_id, sort_sql):
    context = {}
    cursor = connection.cursor()

    sql = 'select data_id, user_id, data_name, data_info, timestamp, ' \
          'first_title, second_title, data_type, data_size ' \
          'from BSCapp_sciencedata where BSCapp_sciencedata.user_id != %s and BSCapp_sciencedata.data_status = 1 '
    search_sql = ''

    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'and {} like %s '.format(search_base)
    except Exception as e:
        # print(e)
        pass
    sql = sql + search_sql + sort_sql
    try:
        if search_sql:
            cursor.execute(sql, [buyer_id, "%"+search_field+"%"])
        else:
            cursor.execute(sql, [buyer_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return context
    datas = []
    len_content = len(content)

    for i in range(len_content):
        data = dict()
        data['data_id'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1]).user_name
        data['user_id'] = seller
        data['data_name'] = content[i][2]
        data['data_info'] = content[i][3]
        data['timestamp'] = time_to_str(content[i][4])
        data['first_title'] = content[i][5]
        data['second_title'] = content[i][6]
        data['data_type'] = content[i][7]
        data_size = content[i][8]

        if data_size < 1:
            data['data_size'] = str(round(data_size * 1024.0, 3)) + ' KB'
        else:
            data['data_size'] = str(round(data_size, 3)) + ' MB'
        datas.append(data)
    return datas, len_content

def orderData_sql(request, user_id, sort_sql):

    context = {}
    cursor = connection.cursor()
    sql = 'select BSCapp_data.data_id,BSCapp_data.user_id, BSCapp_data.data_name, BSCapp_data.data_info,BSCapp_data.data_source,' \
          'BSCapp_data.data_type, BSCapp_transaction.timestamp, BSCapp_transaction.price, BSCapp_data.data_address, ' \
          'BSCapp_data.data_score, BSCapp_data.comment_number, BSCapp_transaction.data_score ' \
          'from BSCapp_data, BSCapp_transaction ' \
          'where BSCapp_data.data_id = BSCapp_transaction.data_id and BSCapp_transaction.buyer_id = %s '
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'and {} like %s '.format(search_base)
    except:
        pass
    sql = sql + search_sql + sort_sql
    try:
        if search_sql:
            cursor.execute(sql, [user_id, "%"+search_field+"%"])
        else:
            cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
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
        order['address'] = content[i][8]
        data_avg_score = content[i][9]
        comment_number = content[i][10]
        if comment_number == 0 or data_avg_score == 0.0:
            order['avg_score'] = '0 (暂无评级)'
            order['comment_number'] = '0 '
        else:
            order['avg_score'] = data_avg_score
            order['comment_number'] = comment_number
        data_score = content[i][11]
        if data_score ==0:
            order['self_score'] = 0
        else:
            order['self_score'] = data_score

        orders.append(order)
    return orders

def uploadData_sql(request, user_id, sort_sql):
    context = {}
    cursor = connection.cursor()
    sql = 'select data_name, data_info, timestamp, first_title, second_title, ' \
          'data_type, data_status, data_size ' \
          'from BSCapp_sciencedata where BSCapp_sciencedata.user_id = %s '
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'and {} like %s '.format(search_base)
    except:
        pass
    sql = sql + search_sql + sort_sql
    # print(sql)
    try:
        if search_sql:
            cursor.execute(sql, [user_id, "%" + search_field + "%"])
        else:
            cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return context
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['data_name'] = content[i][0]
        data['data_info'] = content[i][1]
        data['timestamp'] = time_to_str(content[i][2])
        data['first_title'] = content[i][3]
        data['second_title'] = content[i][4]
        data['data_type'] = content[i][5]
        # status = 0 审核中
        # status = 1 审核通过
        # status = 2 审核不通过
        if content[i][6] == 0:
            data['data_status'] = '审核中'
        elif content[i][6] == 1:
            data['data_status'] = '审核通过'
        else:
            data['data_status'] = '审核不通过'
        data['data_size'] = content[i][7]
        data_size = data['data_size']
        if data_size < 1 :
            data['data_size'] = str(round(data_size * 1024.0,3)) + ' KB'
        else:
            data['data_size'] = str(round(data_size, 3)) + ' MB'

        datas.append(data)
    return datas, len_content

def adminData_sql(request, sort_sql):
    cursor = connection.cursor()
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'where {} like %s '.format(search_base)
    except Exception as e:
        # print(e)
        pass
    sql = 'select data_id, user_id, timestamp, data_name, data_source,   \
           data_info, data_type, first_title, second_title, data_status, data_size ' \
          ' from BSCapp_sciencedata '
    sql = sql + search_sql + sort_sql
    # print(sql)
    try:
        if search_sql:
            cursor.execute(sql, ["%"+search_field+"%"])
        else:
            cursor.execute(sql) 
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return {}
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['data_id'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1])
        data['user_id'] = seller.user_name
        data['timestamp'] = time_to_str(content[i][2])
        data['data_name'] = content[i][3]
        data['data_source'] = content[i][4]
        data['data_info'] = content[i][5]
        data['data_type'] = content[i][6]
        data['first_title'] = content[i][7]
        data['second_title'] = content[i][8]

        if content[i][9] == 0:
            data['data_status'] = '审核中'
        elif content[i][9] == 1:
            data['data_status'] = '审核通过'
        else:
            data['data_status'] = '审核不通过'

        data['data_size'] = round((float)(content[i][10]),5)
        data_size = data['data_size']
        if data_size < 1 :
            data['data_size'] = str(round(data_size * 1024.0,3)) + ' KB'
        else:
            data['data_size'] = str(round(data_size , 3)) + ' MB'
        datas.append(data)

    return datas

def txLog_sql(user_id):
    content = {}
    cursor = connection.cursor()
    sql = 'select science_data_id, timestamp, action ' \
          'from BSCapp_downloadLog where BSCapp_downloadLog.user_id = %s order by timestamp DESC;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    tx_logs = []
    for i in range(len(content)):
        tx_log = dict()
        sciencd_data = ScienceData.objects.get(data_id=content[i][0])
        tx_log['science_data_id'] = sciencd_data.data_name
        tx_log['timestamp'] = time_to_str(content[i][1])
        tx_log['first_title'] = sciencd_data.first_title
        tx_log['second_title'] = sciencd_data.second_title
        tx_log['data_source'] = sciencd_data.data_source
        tx_log['data_type'] = sciencd_data.data_type
        tx_log['action'] = content[i][2]
        tx_logs.append(tx_log)
    return tx_logs
#
# def rechargeData_sql(user_id):
#     content = {}
#     cursor = connection.cursor()
#     sql = 'select timestamp,credits,before_account,after_account from BSCapp_recharge where BSCapp_recharge.user_id = %s order by timestamp DESC;'
#     try:
#         cursor.execute(sql, [user_id])
#         content = cursor.fetchall()
#         cursor.close()
#     except Exception as e:
#         cursor.close()
#     recharges = []
#     for i in range(len(content)):
#         recharge = dict()
#         recharge['timestamp'] = time_to_str(content[i][0])
#         recharge['credits'] = content[i][1]
#         recharge['before_account'] = content[i][2]
#         recharge['after_account'] = content[i][3]
#         recharges.append(recharge)
#     return recharges


def noticeData_sql(user_id, sort_sql):
    content = {}
    cursor = connection.cursor()
    sql = 'select notice_id, sender_id, notice_type, notice_info, timestamp, if_check from BSCapp_notice where receiver_id = %s and if_delete = False '

    sql = sql + sort_sql
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return content
    notices = []
    len_content = len(content)
    unread_number = 0
    unread_notices = []
    show_unread_number = 5

    for i in range(len_content):
        notice = dict()
        notice['notice_id'] = content[i][0]
        sender_id = content[i][1]
        notice_type = content[i][2]
        if notice_type == 1 or notice_type == 2: # review pass or reject
            notice['sender'] = Admin.objects.get(admin_id=sender_id).admin_name
        elif notice_type == 3 or  notice_type == 4: # recharge success
            notice['sender'] = '系统'
        else:
            notice['sender'] = '系统'
        notice['info'] = content[i][3]
        notice['timestamp'] = time_to_str(content[i][4])
        if_check= content[i][5]
        if if_check == True:
            notice['if_check'] = '已读'
        else:
            notice['if_check'] = '未读'
            unread_number+=1
            if (unread_number <= show_unread_number):
                unread_notices.append(notice)
        notices.append(notice)

    return notices, unread_notices, unread_number

# Done add config number = 7
def pagingData(request, datas, each_num=7):
    # paginator = Paginator(datas, each_num)
    # print(each_num)
    paginator = JuncheePaginator(datas, each_num)
    page = request.GET.get('page', 1)
    try:
        paged_recharges = paginator.page(page)
    except PageNotAnInteger:
        paged_recharges = paginator.page(1)
    except EmptyPage:
        paged_recharges = paginator.page(paginator.num_pages)
    return paged_recharges


def get_notices(request, user_id):
    Notice_sort_name_and_type = request.session['Notice_sort_name_and_type']
    result = Notice_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    table_name = 'BSCapp_notice'
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)
    notices, unread_notices, unread_number = noticeData_sql(user_id, sort_sql)
    return notices, unread_notices, unread_number

def GetUploadData(user_id):
    #get upload data
    content = {}
    cursor = connection.cursor()
    sql = 'select data_id from BSCapp_sciencedata where BSCapp_sciencedata.user_id = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    return content

def GetDownloadData(user_id):
    #get purchase data
    content = {}
    cursor = connection.cursor()
    sql = 'select log_id from BSCapp_downloadlog where BSCapp_downloadlog.user_id = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    return content

def GetPurchaseData(user_id):
    #get purchase data
    content = {}
    cursor = connection.cursor()
    sql = 'select data_id from BSCapp_purchase where BSCapp_purchase.user_id = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    return content

def generate_sort_class(sort_name, sort_type, sort_list):
    sort_class = {}
    for item in sort_list :
        sort_class[item] = ''

    if sort_type == 'DESC':
        sort_class[sort_name] = 'fa fa-caret-down text-danger' # DESC down
    else:
        sort_class[sort_name] = 'fa fa-caret-up text-success' # ASC up
    return sort_class

def chainData_sql(request, sort_sql):
    context = {}
    cursor = connection.cursor()
    sql = 'select height, timestamp, block_size, tx_number, block_hash ' \
          'from BSCapp_block '

    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'where {} like %s '.format(search_base)
    except Exception as e:
        # print(e)
        pass

    sql = sql + search_sql + sort_sql
    try:
        if search_sql:
            cursor.execute(sql, ["%"+search_field+"%"])
        else:
            cursor.execute(sql)
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return context

    blocks = []
    len_content = len(content)
    for i in range(len_content):
        block = dict()
        block['height'] = content[i][0]
        block['timestamp'] = time_to_str(content[i][1])
        block['block_size'] = content[i][2]
        block['tx_number'] = content[i][3]
        block['block_hash'] = content[i][4]
        block['wholeInfo'] = get_block_by_index_json(content[i][0])

        for i in range(block['tx_number']):
            timestamp = block['wholeInfo']['transactions'][i]['timestamp']
            block['wholeInfo']['transactions'][i]['timestamp'] = time_to_str(timestamp)

            seller = block['wholeInfo']['transactions'][i]['seller']
            try:
                block['wholeInfo']['transactions'][i]['seller'] = User.objects.get(user_id=seller).user_name
            except:
                pass

            buyer = block['wholeInfo']['transactions'][i]['buyer']
            try:
                block['wholeInfo']['transactions'][i]['buyer'] = User.objects.get(user_id=buyer).user_name
            except:
                pass

            data_uuid = block['wholeInfo']['transactions'][i]['data_uuid']
            try:
                block['wholeInfo']['transactions'][i]['data_uuid'] = Data.objects.get(data_id=data_uuid).data_name
            except:
                pass
            try:
                block['wholeInfo']['transactions'][i]['credit'] = Data.objects.get(data_id=data_uuid).data_price
            except:
                pass
        blocks.append(block)

    return blocks, len_content

def sendResetPwdEmail(receiver, secretKey):

    BSC_ip = 'http://' + '127.0.0.1'
    BSC_port = '8000'

    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "bsc_admin@126.com"  # 用户名
    mail_pass = "bscadmin2018"  # 口令
    receivers = []
    receivers.append(receiver)

    reset_path = BSC_ip + ':' + BSC_port + '/' + str(secretKey)

    message = MIMEText('本邮件发送时间: '+time_to_str(time())+' 重设密码链接: '+reset_path + '  请勿回复本邮件，30分钟后此链接将会失效.', 'plain', 'utf-8')
    message['From'] = mail_user
    message['To'] = receiver
    subject = '重置密码( BSC系统 )'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        return True
    except smtplib.SMTPException as e:
        return False

