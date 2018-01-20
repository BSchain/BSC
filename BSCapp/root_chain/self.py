# -*- coding: utf-8 -*-
# @Time    : 04/01/2018 4:18 PM
# @Author  : 伊甸一点
# @FileName: self.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from time import  time
import json
import hashlib as hasher
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests
import os
import random


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)
        # get chain from file
        # self.generate_chain_from_file()
        # # store
        # self.store_chain()
        self.chain_init()
        # self.generate_chain_from_file()

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_transaction(self,data_seller, data_buyer, data_uuid, credit, action):
        self.current_transactions.append(
            {
                'data_seller': data_seller,
                'data_buyer': data_buyer,
                'data_uuid': data_uuid,
                'credit': credit,
                'action': action
            }
        )
        return self.last_block['index']+1

    def new_block(self, proof, previous_hash = None):
        block ={
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_str = json.dumps(block,sort_keys=True).encode()
        return hasher.sha256(block_str).hexdigest()

    @staticmethod
    def get_diff(block):
        return 10 # diff

    def proof_of_work(self, last_proof,diff=5):
        proof = 0
        while (self.valid_proof(last_proof, proof,diff) is False):
            proof = proof + 1
        return proof

    @staticmethod
    def valid_proof(last_proof,proof,diff=4):
        mine = f'{last_proof}{proof}'.encode()
        mine_hash = hasher.sha256(mine).hexdigest()
        diff_str = '0'*diff
        return mine_hash[:diff] == diff_str

    def chain_init(self,file_name='_blockchain2.json'):
        if os.path.exists(file_name):
            self.generate_chain_from_file(file_name)
            self.store_chain(file_name)
        else:
            self.store_chain(file_name)
            self.generate_chain_from_file(file_name)

    def generate_chain_from_file(self,file_name='_blockchain2.json'):
        with open(file_name,'r') as f:
            self.chain = json.load(f)

    def store_chain(self,file_name='_blockchain2.json'):
        with open(file_name, 'w') as json_file:
            json_file.write(json.dumps(self.chain))


app = Flask(__name__)#  app = django.setup()
node_uuid = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/mine',methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    ts_num = random.randint(1,3)
    for i in range(ts_num):
        blockchain.new_transaction(
            data_seller="buaa",
            data_buyer=node_uuid,
            credit=random.uniform(0,3),
            data_uuid=random.choice(["buaa","zpfbuaa","blockchain","unknown","hahahaha"]),
            action=random.choice(["download","upload","pass","cancle"]),
        )
    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'timestamp': block['timestamp'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    blockchain.store_chain()
    return jsonify(response), 200


@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['data_seller', 'data_buyer', 'data_uuid', 'credit']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['data_seller'], values['data_buyer'], values['data_uuid'], values['credit'])
    response = {'message': f'Transaction will be added to Block {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    # register nodes
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    # store chain
    blockchain.store_chain()
    print('store success')
    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8890, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port)