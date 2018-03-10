# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:16 PM
# @Author  : 伊甸一点
# @FileName: mine.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from BSCapp.root_chain.chain import *

# type block_chain is class <chain>
def mine(block_chain): # need to consider some condition
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
        # last_block = block_chain.chain[-1] # get last block json

        last_block = block_chain.last_block # get last block json
        last_nonce = last_block['nonce'] # get last_nonce
        prev_hash = hash_block(last_block) # calculate the hash for now block
        nonce = proof_of_work(last_nonce) # get proof of work

        # new_block_index = len(block_chain.chain) + 1 # get block height

        new_block_index = block_chain.chain_length + 1 # new block height = chain_length + 1

        block = Block()
        block.new_block(index=new_block_index, timestamp=time(), prev_hash=prev_hash, transactions=block_chain.current_transactions,nonce=nonce)
        block_size = block.save_block() # save to file (one block one file KB)
        now_timestamp = time()
        block_chain.reset_transaction() # reset the current_transaction
        block_chain.chain_length += 1 # add chain_length
        block_chain.last_block = block.to_dict() # update the last block
        if new_block_index % 5 == 0:
            block_chain.get_block_from_to(new_block_index - 4, new_block_index) # only check the 4 blocks
            if block_chain.is_valid():
                print('current chain is valid, the chain height is ', new_block_index)  # valid the chain
            block_chain.reset_chain() # reset the chain to reduce the memory.

        block_chain.chain.append(block.to_dict()) # add the new block to now block_chain

        return new_block_index, now_timestamp, block_size, hash_block(block.to_dict())

    except Exception as e:
        print(str(e))