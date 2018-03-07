# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:02 PM
# @Author  : 伊甸一点
# @FileName: chain.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from BSCapp.root_chain.block import *
import requests
from BSCapp.root_chain.utils import *
import BSCapp.root_chain.transaction as TX
import math

class Chain:
    def __init__(self):
        # 1.the block_length indicate the last_block
        # 2.can also using file_list to valid the block
        # 3.save memory
        # 4.only read total chain when chain needed
        self.chain = [] # TODO: change to record the length of block
        self.current_transactions = []
        self.nodes = set()
        self.chain_length = 0
        self.last_block = '' # json_block

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __le__(self, other):
        pass

    def valid_from_to(self,start_height, end_height): # TODO: valid the block from start_idx to end_idx
        assert start_height <= end_height, ('start height must less than end height', start_height, end_height)
        assert start_height <= self.chain_length, ('start height must less than chain_length', start_height, self.chain_length)
        assert end_height <= self.chain_length, ( 'end height must less than chain_length', end_height, self.chain_length)
        return valid_chain_index(self.chain, start_height, end_height)
        pass

    def is_valid(self):
        return valid_chain(self.chain) # TODO: can change to valid_from_to(self,0, chain_length)
        pass

    def init_chain_length(self):
        assert os.path.exists(BLOCK_SAVE_ROOT), ('blocks save file not exist')
        block_list = os.listdir(BLOCK_SAVE_ROOT)
        self.chain_length = len(block_list)

    def save_chain(self):
        assert os.path.exists(BLOCK_SAVE_ROOT), ('blocks save file not exist')
        for index,each_block in enumerate(self.chain):
            block_file = get_block_file(index+1)
            f = open(block_file,'w')
            f.write(json.dumps(self.chain))
            f.close()

    def reset_chain(self):
        self.chain = [] # can get chain by different way, need to add reset function

    @staticmethod
    def get_gensis_block(gensis_index = 1):
        assert os.path.exists(BLOCK_SAVE_ROOT), ('blocks file not exist')
        with open(get_block_file(gensis_index)) as f:
            gensis_json_block = json.load(f)
        return gensis_json_block # get gensis json block

    def find_block_by_index(self, index):
        assert int(index) > 0, ('index must greater than 0')
        assert int(index) >= self.chain_length, ('index must smaller than chain_length',index,self.chain_length)
        block_file = get_block_file(index)
        assert os.path.exists(block_file), (block_file,'not exist')
        with open(block_file, 'r') as f:
            json_block = json.load(f)
        return json_block

    # use a file to store index and hash
    # def find_block_by_hash(self, hash):
    #     pass

    def get_block_from_to(self, start_height, end_height):
        assert os.path.exists(BLOCK_SAVE_ROOT), ('blocks file not exist')
        for index in range(start_height, end_height + 1): # only get block from [start, end]
            with open(get_block_file(index)) as f:
                json_block = json.load(f)
            self.chain.append(json_block)

    def get_total_chain(self):
        assert os.path.exists(BLOCK_SAVE_ROOT), ('blocks file not exist')
        block_list = os.listdir(BLOCK_SAVE_ROOT)
        for each_block in block_list:
            with open(BLOCK_SAVE_ROOT+each_block,'r') as f:
                json_block = json.load(f)
            self.chain.append(json_block)

    def get_last_block(self):
        self.init_chain_length() # chain_length equal to the number of block
        last_block_file = get_block_file(self.chain_length)
        with open(last_block_file,'r') as f:
            json_block = json.load(f)

        self.last_block = json_block # get the last json block

    def get_current_transaction(self, deleteFile):
        assert os.path.exists(TRANSACTION_SAVE_ROOT), ('blocks file not exist')
        transaction_list = os.listdir(TRANSACTION_SAVE_ROOT)
        for each_transaction in transaction_list: # get the total transaction
            tx_file = TRANSACTION_SAVE_ROOT + each_transaction
            with open(tx_file, 'r') as f:
                transaction = json.load(f)
            self.current_transactions.append(transaction)
            # tx = TX.Transaction.json_to_transaction(transaction)
            if deleteFile:
                # if tx.valid_transaction() :
                os.remove(tx_file)

    def add_block(self,block): # save block to file and add block to chain
        block.save_block()
        self.chain.append(block.to_dict())

    def add_transaction(self,transaction):
        self.current_transactions.append(transaction.to_dict())

    def reset_transaction(self): # when mining a new block, then empty the current_transaction
        self.current_transactions = []

    def generate_block(self, nonce, prev_hash): # generate according to nonce and prev_hash
        # 1. new block
        # 2. prepare parameters
        # 3. save_block to file
        # 4. add block to chain
        block = Block()
        index = len(self.chain) + 1
        timestamp = time()
        transactions = self.current_transactions
        block.new_block(index,timestamp,prev_hash,transactions,nonce)
        block.save_block()
        self.chain.append(block.to_dict()) # be careful, use to_dict

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain') # TODO: need to change with the request

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False