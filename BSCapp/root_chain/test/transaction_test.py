# -*- coding: utf-8 -*-
# @Time    : 07/01/2018 10:53 PM
# @Author  : 伊甸一点
# @FileName: transaction_test.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from transaction import *

# test transaction

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

ts = Transaction()
ts.new_transaction(in_coins, out_coins, timestamp, action, seller, buyer, data_uuid, credit)

print(ts.to_dict())
