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

file_name = 'almost_final_data.csv'
csv_reader = csv.reader(open(file_name,'r'))

header = ['tx_id', 'user_id', 'timestamp', 'science_data_id_list',
          'conference_data_id_list', 'journal_data_id_list', 'patent_data_id_list',
          'action', 'first_title','second_title','data_type']

can_use_user_id = ['e24ac7ba-a31c-3721-85fc-8f99813afbb1', '2b316fd2-1500-3f39-a8db-a786f789e04b', '2a528fad-f1db-3c5c-8ee0-cadd46f53492']


def generate_data(data_round, delete_header = True):
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
        timestamp = str(datetime.datetime.utcnow().timestamp() - 4320000 + number * 120 + random.randint(0,30))
        print(time_to_str(timestamp))
        row[0] = tx_id
        row[1] = user_id
        row[2] = timestamp
        csv_writer.writerow(row)

        # generate logs files
        log = LOG.Logs()
        log.new_log(tx_id=row[0], user_id=row[1], timestamp=row[2],
                science_data_id_list=row[3], conference_data_id_list=row[4], journal_data_id_list=row[5], patent_data_id_list=row[6],
                action=row[7], first_title=row[8], second_title= row[9], reviewer= row[10], data_type=row[11])
        log.save_log()
        # update numbers
        number += 1



generate_data(data_round=0, delete_header=True)

# def start_generate():
#     while(True):
#         data_round = 0
#         generate_data(data_round, delete_header=True)
#         data_round += 1
#         if(data_round > 10):
#             break
#
# start_generate()