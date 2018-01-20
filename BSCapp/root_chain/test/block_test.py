# -*- coding: utf-8 -*-
# @Time    : 07/01/2018 10:53 PM
# @Author  : 伊甸一点
# @FileName: block_test.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from block import *

# test block

action = 'buy'
seller = '111111'
buyer = '000000'

coin1 = Coin()
coin1.new_coin(1,1.2,buyer)

coin2 = Coin()
coin2.new_coin(2,2.2,buyer)

coin3 = Coin()
coin3.new_coin(3,3.4,seller)

in_coins = []
in_coins.append(coin1.to_dict())
in_coins.append(coin2.to_dict())

out_coins = []
out_coins.append(coin3.to_dict())

timestamp = time()
credit = 3.4
data_uuid = str(uuid4()).replace('-','')

ts1 = Transaction()
ts1.new_transaction(in_coins, out_coins, timestamp, action, seller, buyer, data_uuid, credit)

ts2 = Transaction()
ts2.new_transaction(in_coins, out_coins, timestamp, action, seller, buyer, data_uuid, credit)

timestamp2 = time()

# prev_hash = hasher.sha256(('1').encode('utf-8')).hexdigest()
prev_hash= '262aaa2e55f334c5fc6e11edaeeba4e777b67af9867414882a6e21cc43162f27'

transactions = []
transactions.append(ts1.to_dict())
transactions.append(ts2.to_dict())

index = 1
nonce = 100
# index = 2
# nonce = need to change according to block.hash_self

block = Block()
block.new_block(index, timestamp2, prev_hash, transactions, nonce)
block.save_block()
print(block.to_dict())
print(block.hash_self)


