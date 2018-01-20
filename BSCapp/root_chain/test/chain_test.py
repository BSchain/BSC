# -*- coding: utf-8 -*-
# @Time    : 07/01/2018 10:53 PM
# @Author  : 伊甸一点
# @FileName: chain_test.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io
from chain import *

#create two block by hand
# nonce = 100 next_nonce = 888273 is valid (diff=5)
science_chain = Chain()
science_chain.get_total_chain()

if science_chain.is_valid() :
    print('is valid')
else:
    print('not valid')