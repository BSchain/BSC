# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:15 PM
# @Author  : 伊甸一点
# @FileName: utils.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

# TODO: add some methods to this file!

from BSCapp.root_chain.block import *
import json
import hashlib as hasher
import uuid
from time import time

TRANSACTION_SAVE_ROOT = r'transactions/'
TRANSACTION_SAVE_SUFFIX = '.json'
BLOCK_SAVE_ROOT = r'blocks/' # the blocks saving root
BLOCK_SAVE_SUFFIX = '.json' # block suffix
BLOCK_SPLIT = '_' # e.g.  1_hash.json  2018_hash.json (index + '_' + hash + '.json')


def hash_block(block): # json block
    block_str = json.dumps(block, sort_keys=True).encode() # here generate the block string
    return str(hasher.sha256(block_str).hexdigest())


def get_diff(block):
    """
    can use different strategy to generate the diff
    :param block:
    :return:
    """
    return 5 # diff now is set to 5


def proof_of_work(last_nonce, diff=5):
    nonce = 0
    while (valid_nonce(last_nonce, nonce, diff=diff) is False):
        nonce = nonce + 1
    return nonce


def valid_nonce(last_nonce, nonce, diff=5):
    mine = f'{last_nonce}{nonce}'.encode()
    mine_hash = hasher.sha256(mine).hexdigest()
    return mine_hash[:diff] == '0' * diff


# return to json_block
def get_block_by_index_json(index):
    block_file = get_block_file(index)
    assert os.path.exists(block_file), (block_file, 'not exist')
    with open(block_file, 'r') as f:
        json_block = json.load(f)
    return json_block


def get_block_by_index_object(index):
    return Block.json_to_bloc(get_block_by_index_json(index))


def get_block_file(index):
    return BLOCK_SAVE_ROOT + str(index) + BLOCK_SAVE_SUFFIX


def get_total_tx():
    tx_total = []
    tx_files = get_tx_files()
    for item_file in tx_files:
        with open(item_file, 'r') as f:
            item_tx = json.load(f)
        tx_total.append(item_tx)
    return tx_total


def get_n_tx(tx_number,get_total=0):
    tx_sub = []
    tx_files = get_tx_files()
    if get_total == 1:
        return get_total_tx()
    else:
        for idx, item_file in enumerate(tx_files):
            if idx+1 > tx_number:
                return tx_sub
            with open(item_file, 'r') as f:
                item_tx = json.load(f)
            tx_sub.append(item_tx)


def get_tx_number():
    return len(get_tx_files())


def get_tx_files():
    assert os.path.exists(TRANSACTION_SAVE_ROOT), (TRANSACTION_SAVE_ROOT,'not exist')
    tx_files = os.listdir(TRANSACTION_SAVE_ROOT)
    return tx_files


def valid_block(block):
    if block.index == 1:
        return True
    prev_index = block.index - 1
    nonce = block.nonce
    last_nonce = get_block_by_index_object(prev_index).nonce
    return valid_nonce(last_nonce=last_nonce, nonce=nonce)


def valid_chain(chain):
    last_block = chain[0]
    current_index = 1

    while current_index < len(chain):
        block = chain[current_index]
        # print(f'{last_block}')
        # print(f'{block}')
        # print("\n-----------\n")
        # Check that the hash of the block is correct
        print(block['prev_hash'],hash_block(last_block))
        if block['prev_hash'] != hash_block(last_block):
            return False
        print(last_block['nonce'],block['nonce'])
        # Check that the Proof of Work is correct
        if not valid_nonce(last_block['nonce'], block['nonce']):
            print('here!!!')
            return False

        last_block = block
        current_index += 1
    return True


def generate_uuid(name):
    return str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=name))
