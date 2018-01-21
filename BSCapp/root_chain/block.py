# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:02 PM
# @Author  : 伊甸一点
# @FileName: block.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

import os
from BSCapp.root_chain.utils import *

class Block:
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

    def __repr__(self):
        pass

    def __eq__(self,other):
        return self.index == other.index and \
            self.timestamp == other.timestamp and \
            self.prev_hash == other.prev_hash and \
            self.transactions == other.transcations and \
            self.nonce == other.nonce

    def __ne__(self, other_block):
        return self.__eq__(other_block)

    def __gt__(self, other_block):
        return self.index > other_block.index

    def __lt__(self, other_block):
        return self.index < other_block.index

    def save_block(self):
        assert os.path.exists(BLOCK_SAVE_ROOT) , ('Blocks save root file not exist')
        # path = 'blocks/' + str(index) + '_' + str(block_hash) + '.json'
        #save_block_path = config.BLOCK_SAVE_ROOT+ str(self.index)+config.BLOCK_SPLIT+str(self.hash_self) + config.BLOCK_SAVE_SUFFIX
        # path = 'blocks/' + str(index) + '.json'
        save_block_path = BLOCK_SAVE_ROOT+ str(self.index) + BLOCK_SAVE_SUFFIX
        with open(save_block_path, 'w') as json_file:
            json_file.write(json.dumps(self.to_dict()))

    def to_dict(self): # don't have self.hash_self
        block = {
            'index': self.index,
            'timestamp': self.timestamp,
            'prev_hash': self.prev_hash,
            'transactions': self.transactions,
            'nonce': self.nonce,
        }
        return block

    def is_valid(self,prev_block):
        pass

    def new_block(self, index, timestamp, prev_hash, transactions, nonce):
        self.index = index
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash_self = hash_block(self.to_dict())


    @staticmethod
    def json_to_bloc(block_json):
        """
        index
        timestamp
        transactions
        prev_hash
        nonce
        :param block_json:
        :return:
        """
        block = Block()
        block.index = block_json['index']
        block.timestamp = block_json['timestamp']
        block.transactions = block_json['transactions']
        block.prev_hash = block_json['prev_hash']
        block.nonce = block_json['nonce']
        # calculate the hash_self
        block.hash_self = hash_block(block_json)
        return block