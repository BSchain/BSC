# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:16 PM
# @Author  : 伊甸一点
# @FileName: mine.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from BSCapp.root_chain.chain import *

# type block_chain is class <chain>
def mine(block_chain, deleteFile=True): # TODO: need to consider some condition
    """
    transaction
    :param in_coins:
    :param out_coins:
    :param timestamp:
    :param action:
    :param seller:
    :param buyer:
    :param data_uuid:
    :param credit:
    :return:
    """
    try:
        # We run the proof of work algorithm to get the next proof...
        last_block = block_chain.chain[-1] # get last block json
        last_nonce = last_block['nonce'] # get last_nonce

        prev_hash = hash_block(last_block) # calculate the hash for now block

        nonce = proof_of_work(last_nonce) # get proof of work
        index = len(block_chain.chain) + 1 # get block height

        block = Block()
        # transactions = 20
        # or other
        block.new_block(index=index, timestamp=time(), prev_hash=prev_hash, transactions=block_chain.current_transactions,nonce=nonce)
        block.save_block() # save to file (one block one file)
        block_chain.reset_transaction(deleteFile) # reset the current_transaction and delete the file
        if block_chain.is_valid():
            print('current chain is valid, the chain length is ', len(block_chain.chain))  # valid the chain
            block_chain.chain.append(block.to_dict()) # add the new block to now block_chain
        return True
    except Exception as e:
        print(str(e))
        return False