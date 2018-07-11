# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 下午3:14
# @Author  : 伊甸一点
# @FileName: generate_op_files.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

import csv
import random
from BSCapp.root_chain.utils import *
import BSCapp.Logs as LOG
import pymysql

file_name = 'almost_final_data.csv'
csv_reader = csv.reader(open(file_name,'r'))

header = ['tx_id', 'user_id', 'timestamp', 'science_data_id_list',
          'conference_data_id_list', 'journal_data_id_list', 'patent_data_id_list',
          'action', 'first_title','second_title','data_type']

can_use_user_id = ['e24ac7ba-a31c-3721-85fc-8f99813afbb1', '2b316fd2-1500-3f39-a8db-a786f789e04b', '2a528fad-f1db-3c5c-8ee0-cadd46f53492']


def generate_data(data_round, delete_header = True, save_log = True):
    csv_writer = csv.writer(open('final_data'+str(data_round)+'.csv', 'w'))
    first = True
    number = 0
    for row in csv_reader:
        if first:
            if delete_header == False:
                csv_writer.writerow(row)
            first = False
            continue
        user_id = can_use_user_id[random.randint(0,2)]
        tx_id = generate_uuid(user_id)
        # timestamp = str(datetime.datetime.utcnow().timestamp() + number * random.randint(0,10))
        timestamp = str(datetime.datetime.utcnow().timestamp() - 4320000 -86400*data_round + number * 120 + random.randint(0,30))
        print(time_to_str(timestamp))
        row[0] = tx_id
        row[1] = user_id
        row[2] = timestamp
        csv_writer.writerow(row)

        # generate logs files
        if (save_log == True):
            log = LOG.Logs()
            log.new_log(tx_id=row[0], user_id=row[1], timestamp=row[2],
                    science_data_id_list=row[3], conference_data_id_list=row[4], journal_data_id_list=row[5], patent_data_id_list=row[6],
                    action=row[7], first_title=row[8], second_title= row[9], reviewer= row[10], data_type=row[11])
            log.save_log()
        # update numbers
        number += 1


def sql_to_log():
    try:
        db = pymysql.connect(host="localhost", user="root", password="zpflyfe", db="bsc_db", port=3306)
        cursor = db.cursor()
        sql = 'select tx_id, user_id, timestamp, science_data_id_list, conference_data_id_list, journal_data_id_list, ' \
              ' patent_data_id_list, action, first_title, second_title,reviewer, data_type ' \
              'from BSCapp_OperationLog '
        cursor.execute(sql)
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(e)

    len_content = len(content)
    print(len_content)
    for i in range(0, len_content):
        tx_id = content[i][0]
        user_id = content[i][1]
        timestamp = content[i][2]
        science_data_id_list = content[i][3]
        conference_data_id_list = content[i][4]
        journal_data_id_list = content[i][5]
        patent_data_id_list = content[i][6]
        action = content[i][7]
        first_title = content[i][8]
        second_title = content[i][9]
        reviewer = content[i][10]
        data_type = content[i][11]
        log = LOG.Logs()
        log.new_log(tx_id=tx_id, user_id=user_id, timestamp=timestamp,
                    science_data_id_list=science_data_id_list, conference_data_id_list=conference_data_id_list,
                    journal_data_id_list=journal_data_id_list, patent_data_id_list=patent_data_id_list,
                    action=action, first_title=first_title, second_title=second_title, reviewer=reviewer, data_type=data_type)
        log.save_log()


# sql_to_log()
# generate_data(data_round=5, delete_header=True, save_log = True)





# def start_generate():
#     while(True):
#         data_round = 0
#         generate_data(data_round, delete_header=True)
#         data_round += 1
#         if(data_round > 10):
#             break
#
# start_generate()