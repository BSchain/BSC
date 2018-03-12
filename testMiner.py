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

# TODO: syn total chain data to DB
# one week = 24*60*60*7
def chainDataSynToDB():
    assert os.path.exists(UTILS.BLOCK_SAVE_ROOT), ('blocks file not exists!')
    total_file = os.listdir(UTILS.BLOCK_SAVE_ROOT)

    coin_dict = {} # total coin status
    # key: coin_uuid
    # value: (coin_number, coin_owner, is_spent)

    for item in total_file:
        with open(UTILS.BLOCK_SAVE_ROOT + item, 'r') as f:
            block = json.load(f)
        transactions = block['transactions']
        len_transactions = len(transactions)
        for i in range(len_transactions):
            in_coins = transactions[i]['in_coins']
            out_coins = transactions[i]['out_coins']
            len_in_coins = len(in_coins)
            len_out_coins = len(out_coins)

            # out_coins
            for j in range(len_out_coins):
                coin_uuid = out_coins[j]['coin_uuid']
                number_coin = out_coins[j]['number_coin']
                owner = out_coins[j]['owner']
                if coin_dict.__contains__(coin_uuid) == False:
                    coin_dict[coin_uuid] = (number_coin, owner, 0) # coin_number, owner, is_spent = 1

            # in_coins
            for j in range(len_in_coins):
                coin_uuid = in_coins[j]['coin_uuid']
                number_coin = in_coins[j]['number_coin']
                owner = in_coins[j]['owner']
                if coin_dict.__contains__(coin_uuid) :
                    coin_dict[coin_uuid] = (number_coin, owner, 1) # coin_number, owner, is_spent = 0

    # insert or update the coin status
    insert_number = 0
    update_number = 0
    for key_coin_id, coin_value in coin_dict.items():
        try:
            coin_get = "select BSCapp_coin.owner_id from BSCapp_coin where BSCapp_coin.coin_id = %s"
            cursor.execute(coin_get,[key_coin_id])
            content = cursor.fetchall()
            if len(content) == 0:
                try:
                    coin_insert = "insert into BSCapp_coin  \
                                  (coin_id, coin_credit, owner_id, is_spent, timestamp)  \
                                  values ('%s', '%s', '%s', '%s', '%s')" %  \
                                  (key_coin_id, coin_value[0], coin_value[1],coin_value[2], time.time())
                    cursor.execute(coin_insert)
                    db.commit()
                    insert_number+=1
                except Exception as e:
                    db.rollback()
                    print(e)
            else:
                try:
                    coin_update = 'update BSCapp_coin ' \
                      'set BSCapp_coin.coin_credit = %s, BSCapp_coin.owner_id = %s, BSCapp_coin.is_spent = %s ' \
                      'where BSCapp_coin.coin_id = %s'
                    cursor.execute(coin_update, [coin_value[0], coin_value[1], coin_value[2], key_coin_id])
                    db.commit()
                    update_number+=1
                except Exception as e:
                    db.rollback()
                    print(e)
        except Exception as e:
            print(e)
        print("key:",key_coin_id, "value:", coin_value)

    print('insert number: ' +str(insert_number))
    print('update number: ' +str(update_number))
    return coin_dict

def mine_block(mineChain, diff=5, debug = False):
    # mineChain.get_total_chain()  # get total chain
    mineChain.get_last_block() # get the last block

    if debug:
        sleepTime = 10  # change to 10 seconds
        blockSizeLimit = 1024  # now set 1024 B
        synTimeSpan = 60  # one minutes
    else:
        sleepTime = 300  # change to 5 minutes
        blockSizeLimit = 1024 * 10  # now set 1024 * 10 B
        synTimeSpan = 7 * 24 * 60 * 60  # one week to syn data
    last_syn_time = 0

    synCounter = 0
    while True:
        if last_syn_time == 0:
            synCounter += 1
            print('------------------ Syn Data time: ' + str(synCounter) + '----------------')
            chainDataSynToDB()  # the first time syn
            last_syn_time = time.time()

        if time.time() - last_syn_time >= synTimeSpan:
            synCounter += 1
            print('------------------ Syn Data time: ' + str(synCounter) + '----------------')
            chainDataSynToDB()  # the first time syn
            last_syn_time = time.time()

        # get current transaction not contain empty transaction
        mineChain.get_current_transaction(blockSizeLimit, deleteFile=True)
        transaction_number = len(mineChain.current_transactions) # transaction numbers !!!
        if transaction_number == 0 :
            print('now is empty transaction')
            time.sleep(sleepTime)
            continue
        # print(mineChain.current_transactions)
        chain_height, block_timestamp, block_size, now_block_hash = MINE.mine(mineChain, diff=diff) # mine the block
        print('chain_height',chain_height)
        print('block_timestamp', block_timestamp)
        print('block_size',block_size)
        print('now_block_hash',now_block_hash)
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

def run_mine(mineChain, insert_gensis = False, diff=5, debug = False):
    if insert_gensis:
        insert_gensis_block()
    mine_block(mineChain, diff=diff, debug = debug)

mineChain = CHAIN.Chain() # new a init chain
default_debug = True # the debug setting!!!

default_diff = 5 # very quick
# default_diff = 6 #  60 seconds to mine

self_insert_gensis = False
input_str = input('input insert gensis (y: yes, n: no)')
if input_str == 'y' or input_str == 'yes':
    self_insert_gensis = True

run_mine(mineChain, insert_gensis=self_insert_gensis, diff=default_diff, debug=default_debug)