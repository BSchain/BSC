# -*- coding: utf-8 -*-
# @Time    : 05/03/2018 12:02 PM
# @Author  : 伊甸一点
# @FileName: testMiner.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

import BSCapp.root_chain.chain as CHAIN
import BSCapp.root_chain.mine as MINE
import time

mineChain = CHAIN.Chain() # new a init chain
round_number = 0
mineChain.get_total_chain()  # get total chain

while True:
    # get current transaction not contain empty transaction
    mineChain.get_current_transaction()
    if len(mineChain.current_transactions) == 0 :
        print('now is empty transaction')
        time.sleep(600)  # sleep one minute -> change to 10 minutes
        continue
    MINE.mine(mineChain, deleteFile=True) # mine the block

    round_number+=1
    print('round_number:',round_number)
    time.sleep(600)  # sleep one minute -> change to 10 minutes