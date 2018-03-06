# -*- coding: utf-8 -*-
# @Time    : 05/03/2018 12:02 PM
# @Author  : 伊甸一点
# @FileName: testMiner.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io
from __future__ import unicode_literals

import BSCapp.root_chain.chain as CHAIN
import BSCapp.root_chain.mine as MINE
import time
import pymysql

db= pymysql.connect(host="localhost",user="root", password="zpflyfe",db="bsc_db",port=3306)
cursor = db.cursor()

# insert the first block info to database!
# block_insert = "insert into BSCapp_block \
#                         (height, timestamp, block_size, tx_number) \
#                         values ('%d', '%s', '%d', '%d' )" % (chain_height, block_timestamp, block_size, transaction_number)
# cursor.execute(block_insert)
# db.commit()
# print('insert first block!')

mineChain = CHAIN.Chain() # new a init chain
mineChain.get_total_chain()  # get total chain
sleepTime = 60

while True:
    # get current transaction not contain empty transaction
    mineChain.get_current_transaction(deleteFile=True)

    transaction_number = len(mineChain.current_transactions) # transaction numbers !!!

    if transaction_number == 0 :
        print('now is empty transaction')
        time.sleep(sleepTime)  # sleep one minute -> change to 10 minutes
        continue

    chain_height, block_timestamp, block_size, block_info = MINE.mine(mineChain) # mine the block
    print(chain_height, block_timestamp, block_size, block_info)
    # sql = "INSERT INTO BSCapp_block(height, timestamp, block_size, tx_number) VALUES('%d','%s','%d','%d') % (chain_height, block_timestamp, block_size, transaction_number)"
    # sql = "select * from BSCapp_user"
    try:

        block_insert = "insert into BSCapp_block \
                        (height, timestamp, block_size, tx_number) \
                        values ('%d', '%s', '%d', '%d' )" % (chain_height, block_timestamp, block_size, transaction_number)
        cursor.execute(block_insert)
        db.commit()
        print('insert success!')
    except Exception as e:
        print(str(e))
        db.rollback()
        print('insert wrong!!!')
    time.sleep(sleepTime)  # sleep one minute change to 10 minutes