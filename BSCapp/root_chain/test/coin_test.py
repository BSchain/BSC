# -*- coding: utf-8 -*-
# @Time    : 07/01/2018 10:53 PM
# @Author  : 伊甸一点
# @FileName: coin_test.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io
from coin import *

# test coin

coin = Coin()
coin.new_coin(1,1,1)
print(coin.to_dict())
