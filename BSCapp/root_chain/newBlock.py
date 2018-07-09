# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:02 PM
# @Author  : 伊甸一点
# @FileName: block.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

import os
from BSCapp.root_chain.utils import *

class NewBlock:
    def __init__(self):
        self.index = None
        self.timestamp = None
        self.prev_hash = None
        # need to change to list
        # mine only the first 20 or 10 transcations
        self.transactions = []
        self.nonce = None
        # just to calculate the self.hash
        self.hash_self = None

    def new_save_block(self):
        assert os.path.exists(NEW_BLOCK_SAVE_ROOT) , ('Blocks save root file not exist')
        save_block_path = new_get_block_file(self.index)
        with open(save_block_path, 'w') as json_file:
            json_file.write(json.dumps(self.to_dict()))
        return os.path.getsize(save_block_path) # get the block size B

    def to_dict(self): # don't have self.hash_self
        block = {
            'index': self.index,
            'timestamp': self.timestamp,
            'prev_hash': self.prev_hash,
            'transactions': self.transactions,
            'nonce': self.nonce,
        }
        return block

    def new_block(self, index, timestamp, prev_hash, transactions, nonce):
        self.index = index
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash_self = hash_block(self.to_dict())


    @staticmethod
    def json_to_bloc(block_json):
        block = Block()
        block.index = block_json['index']
        block.timestamp = block_json['timestamp']
        block.transactions = block_json['transactions']
        block.prev_hash = block_json['prev_hash']
        block.nonce = block_json['nonce']
        block.hash_self = hash_block(block_json)
        return block