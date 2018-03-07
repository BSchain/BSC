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
import os
import BSCapp.root_chain.utils as UTILS

db= pymysql.connect(host="localhost",user="root", password="zpflyfe",db="bsc_db",port=3306)
cursor = db.cursor()

# insert the first block info to database!
# FIXME: only run following code once!!!
def insert_gensis_block():
    gensis_block = CHAIN.Chain().get_gensis_block()
    gensis_index = 1
    gensis_chain_height = gensis_index
    gensis_block_timestamp = gensis_block['timestamp']
    gensis_block_size = os.path.getsize(UTILS.get_block_file(gensis_chain_height))
    gensis_transaction_number = 0
    gensis_hash = UTILS.hash_block(gensis_block)
    try:

        block_insert = "insert into BSCapp_block \
                        (height, timestamp, block_size, tx_number, block_hash) \
                        values ('%d', '%s', '%d', '%d', '%s')" % \
                       (gensis_chain_height, gensis_block_timestamp, gensis_block_size, gensis_transaction_number, gensis_hash)
        cursor.execute(block_insert)
        db.commit()
        print('insert success!')
    except Exception as e:
        print(str(e))
        db.rollback()
        print('insert wrong!')

def mine_block(mineChain, sleepTime):
    # mineChain.get_total_chain()  # get total chain
    mineChain.get_last_block() # get the last block
    while True:
        # get current transaction not contain empty transaction
        mineChain.get_current_transaction(deleteFile=True)
        transaction_number = len(mineChain.current_transactions) # transaction numbers !!!
        if transaction_number == 0 :
            print('now is empty transaction')
            time.sleep(sleepTime)
            continue
        # print(mineChain.current_transactions)
        chain_height, block_timestamp, block_size, now_block_hash = MINE.mine(mineChain) # mine the block
        print(chain_height, block_timestamp, block_size, now_block_hash)
        try:

            block_insert = "insert into BSCapp_block \
                            (height, timestamp, block_size, tx_number, block_hash) \
                            values ('%d', '%s', '%d', '%d',  '%s')" % \
                           (chain_height, block_timestamp, block_size, transaction_number, now_block_hash)
            cursor.execute(block_insert)
            db.commit()
            print('insert success!')
        except Exception as e:
            print(str(e))
            db.rollback()
            print('insert wrong!')
        time.sleep(sleepTime)

def run_mine(mineChain, sleepTime, insert_gensis = False):
    if insert_gensis:
        insert_gensis_block()
    mine_block(mineChain, sleepTime)

mineChain = CHAIN.Chain() # new a init chain
sleepTime = 10 # change to 10 minutes

self_insert_gensis = False
input_str = input('input insert gensis (y: yes, n: no)')
if input_str == 'y' or input_str == 'yes':
    self_insert_gensis = True

run_mine(mineChain, sleepTime, insert_gensis=self_insert_gensis)