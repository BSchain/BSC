# -*- coding: utf-8 -*-
# @Time    : 01/02/2018 4:25 PM
# @Author  : 伊甸一点
# @FileName: function.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from django.db import connection
from BSCapp.root_chain.utils import *
from BSCapp.models import *

def generate_sort_sql(table_name, sort_name, sort_type):
    sort_sql = 'order by ' + table_name + '.' + sort_name+' '+sort_type+';'
    return sort_sql

def buyData_sql(buyer_id, sort_sql):
    context = {}
    cursor = connection.cursor()
    sql = 'select data_id, user_id, data_name, data_info, timestamp, ' \
          'data_tag, data_status, data_md5, data_size, data_price ' \
          'from BSCapp_data where BSCapp_data.user_id != %s and BSCapp_data.data_status = 1 '

    sql = sql + sort_sql
    try:
        cursor.execute(sql, [buyer_id])
        content = cursor.fetchall()
        cursor.close()
    except:
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
    return datas

def orderData_sql(user_id, sort_sql):

    context = {}
    cursor = connection.cursor()
    sql = 'select BSCapp_data.data_id,BSCapp_data.user_id, BSCapp_data.data_name, BSCapp_data.data_info,BSCapp_data.data_source,' \
          'BSCapp_data.data_type, BSCapp_transaction.timestamp, BSCapp_transaction.price from BSCapp_data \
          ,BSCapp_transaction where BSCapp_data.data_id = BSCapp_transaction.data_id and BSCapp_transaction.buyer_id = %s '

    sql = sql + sort_sql
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
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
        # order['timestamp'] = time_to_str(content[i][6])
        order['timestamp'] = content[i][6]
        order['price'] = content[i][7]
        orders.append(order)
    return orders