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
import json

db= pymysql.connect(host="localhost",user="root", password="zpflyfe",db="bsc_db",port=3306)
cursor = db.cursor()

# insert the first block info to database!
# only run following code once!!!
def insert_gensis_block():
    gensis_block = CHAIN.Chain().new_get_gensis_block()
    gensis_block_height = 1
    gensis_block_timestamp = gensis_block['timestamp']
    gensis_block_prev_hash = gensis_block['prev_hash']
    gensis_block_nonce = gensis_block['nonce']
    gensis_hash = UTILS.hash_block(gensis_block)
    try:
        block_insert = "insert into BSCapp_Newblock \
                        (block_height, prev_hash, block_timestamp, nonce, block_hash, tx_id) \
                        values ('%d', '%s', '%s', '%s', '%s', '%s')" % \
                       (gensis_block_height-1, gensis_block_prev_hash, gensis_block_timestamp, gensis_block_nonce, gensis_hash, '2018')
        cursor.execute(block_insert)
        db.commit()
        print('insert success!')
    except Exception as e:
        print(str(e))
        db.rollback()
        print('insert wrong!')


def mine_block(mineChain, diff=5, debug = False):
    # mineChain.get_total_chain()  # get total chain
    mineChain.new_get_last_block() # get the last block

    if debug:
        sleepTime = 10  # change to 10 seconds
        blockSizeLimit = 1024 * 2   # now set 1024 B

    else:
        sleepTime = 150  # change to 5 minutes
        blockSizeLimit = 1024 * 5  # now set 1024 * 2 B

    while True:
        # get current transaction not contain empty transaction
        mineChain.new_get_current_transaction(blockSizeLimit, deleteFile=True)
        transaction_number = len(mineChain.current_transactions) # transaction numbers !!!
        for i in range(0,transaction_number):
            print(mineChain.current_transactions[i]['timestamp'])
        if transaction_number == 0 :
            print(UTILS.time_to_str(str(time.time())) +' now is empty transaction')
            time.sleep(sleepTime)
            continue
        # print(mineChain.current_transactions)
        tx_id_list = []
        for i in range(0,transaction_number):
            item_tx_id = mineChain.current_transactions[i]['tx_id']
            tx_id_list.append(item_tx_id)
        tx_num = len(tx_id_list)

        chain_height, prev_hash, block_timestamp, nonce , now_block_hash = MINE.mine(mineChain, diff=diff) # mine the block
        # print('chain_height',chain_height)
        # print('prev_hash', prev_hash)
        # print('block_timestamp',block_timestamp)
        # print('nonce',nonce)
        # print('now_block_hash', now_block_hash)
        print('now tx numbers', tx_num)
        print('tx_id_list', tx_id_list)
        for i in range(0, tx_num):
            try:
                tx_id = tx_id_list[i]
                # print(tx_id)
                block_insert = "insert into BSCapp_Newblock \
                                (block_height, prev_hash, block_timestamp, nonce, block_hash, tx_id) \
                                values ('%d', '%s', '%s', '%d',  '%s', '%s')" % \
                               (chain_height-1, prev_hash, block_timestamp, nonce, now_block_hash, tx_id)
                cursor.execute(block_insert)
                db.commit()
                # print(UTILS.time_to_str(str(time.time())) + ' insert success!')
                print(UTILS.time_to_str(str(UTILS.older_time(time.time()))) +' insert success!')
            except Exception as e:
                # print(str(e))
                db.rollback()
                # print(UTILS.time_to_str(str(time.time())) + ' insert wrong!')
                print(UTILS.time_to_str(str(UTILS.older_time(time.time()))) + ' insert wrong!')
        print('Sleeping...')
        time.sleep(sleepTime)


def run_mine(mineChain, insert_gensis = False, diff=5, debug = False):
    if insert_gensis:
        insert_gensis_block()
    mine_block(mineChain, diff=diff, debug = debug)


mineChain = CHAIN.Chain() # new a init chain

default_diff = 5 # very quick
# default_diff = 6 #  60 seconds to mine

self_insert_gensis = False
default_debug = False # the debug setting!!!

input_str = input('input insert gensis (y: yes, n: no)')
if input_str == 'y' or input_str == 'yes':
    self_insert_gensis = True


input_str = input('input debug (y: yes, n: no)')
if input_str == 'y' or input_str == 'yes':
    default_debug = True

run_mine(mineChain, insert_gensis=self_insert_gensis, diff=default_diff, debug=default_debug)