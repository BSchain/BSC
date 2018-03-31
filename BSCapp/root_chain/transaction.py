# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:11 PM
# @Author  : 伊甸一点
# @FileName: transaction.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io
import os
from BSCapp.root_chain.utils import *

class Transaction:
    def __init__(self):
        self.in_coins = []
        self.out_coins = []
        self.timestamp = ''
        self.action = ''
        self.seller = ''
        self.buyer = ''
        self.data_uuid = ''
        self.credit = 0.0
        self.reviewer = ''

    def __eq__(self, other_ts):
        return self.in_coins == other_ts.in_coins and \
            self.out_coins == other_ts.out_coins and \
            self.timestamp == other_ts.timestamp and \
            self.action == other_ts.action and \
            self.seller == other_ts.seller and \
            self.buyer == other_ts.buyer and \
            self.data_uuid == other_ts.data_uuid and \
            self.credit == other_ts.credit and \
            self.reviewer == other_ts.reviewer

    def __ne__(self, other):
        return self.__eq__(other)

    def to_dict(self):
        # change to different kinds of structure
        transaction = {
            'in_coins': self.in_coins,
            'out_coins': self.out_coins,
            'timestamp': self.timestamp,
            'action': self.action,
            'seller': self.seller,
            'buyer': self.buyer,
            'data_uuid': self.data_uuid,
            'credit': self.credit,
            'reviewer': self.reviewer,
        }
        return transaction

    def save_transaction(self):
        if os.path.exists(TRANSACTION_SAVE_ROOT) == False:
            os.mkdir(TRANSACTION_SAVE_ROOT)
        assert os.path.exists(TRANSACTION_SAVE_ROOT), (TRANSACTION_SAVE_ROOT,' not exist')
        # path = 'blocks/' + str(index) + '_' + str(block_hash) + '.json'
        # save_block_path = config.BLOCK_SAVE_ROOT+ str(self.index)+config.BLOCK_SPLIT+str(self.hash_self) + config.BLOCK_SAVE_SUFFIX
        # path = 'blocks/' + str(index) + '.json'
        save_tx_path = TRANSACTION_SAVE_ROOT + str(self.timestamp) + TRANSACTION_SAVE_SUFFIX
        with open(save_tx_path, 'w',encoding='utf-8') as json_file:
            json_file.write(json.dumps(self.to_dict()))

    # can change to init value
    def new_transaction(self, in_coins=None, out_coins=None, timestamp=None,
                        action=None, seller=None, buyer=None, data_uuid=None, credit=None, reviewer=None):
        """

        :param in_coins:
        :param out_coins:
        :param timestamp:
        :param action:
        :param seller:
        :param buyer:
        :param data_uuid:
        :param credit:
        :param reviewer:
        :return:
        """
        self.in_coins=in_coins
        self.out_coins=out_coins
        self.timestamp = timestamp
        self.action = action
        self.seller = seller
        self.buyer = buyer
        self.data_uuid = data_uuid
        self.credit = credit
        self.reviewer = reviewer

    @staticmethod
    def json_to_transaction(transaction_json):
        """

        :param transaction_json:
        :return:
        """
        tx = Transaction()
        tx.in_coins = transaction_json['in_coins']
        tx.out_coins = transaction_json['out_coins']
        tx.timestamp = transaction_json['timestamp']
        tx.action = transaction_json['action']
        tx.seller = transaction_json['seller']
        tx.buyer = transaction_json['buyer']
        tx.data_uuid = transaction_json['data_uuid']
        tx.credit = transaction_json['credit']
        tx.reviewer = transaction_json['reviewer']
        return tx
    """

    卖数据seller = 'zpf_uuid'
    数据uuid = 'mydata_uuid'
    数据信用价格credit = 2.0
    时间戳timestamp = 1515846393.1849742
    买数据buyer = 'buaa_uuid'
    管理员reviewer = 'admin_uuid'

    if action == 'upload' :
        in_coins = []
        out_coins = [{
            coin_uuid: generate_uuid_coin, 
            number_coin: credit( equals to credit) 
            owner: seller ('zpf_uuid')  
        }]
        timestamp = 1515846393.1849742
        action = 'upload'
        seller = 'zpf_uuid'
        buyer = '' 
        data_uuid = 'mydata_uuid'
        credit = 2.0
        reviewer = ''
    if action == 'buy' :
        in_coins = [{
            coin_uuid: 'coin_uuid_1' (unspent)
            number_coin: credit1 (credit1 <= credit)
            owner: seller ('zpfbuaa_uuid') 
        },
        {
            coin_uuid: 'coin_uuid_2' (unspent)
            number_coin: credit2 (credit2 <= credit)
            owner: buyer ('buaa_uuid') 
        },
        {
            coin_uuid: 'coin_uuid_3' (unspent)
            number_coin: credit3 (credit3 <= credit)
            owner: buyer ('buaa_uuid') 
        }] // credit1 + credit2 + credit3 = credit = 2.0
        out_coins = [{
            coin_uuid: generate_uuid_coin, 
            number_coin: credit( equals to credit) 
            owner: buyer ('buaa_uuid') 
        }]
        timestamp = 1515846393.1849742
        action = 'buy'
        seller = 'zpf_uuid'
        buyer = 'buaa_uuid'
        data_uuid = 'mydata_uuid'
        credit = 2.0
        reviewer = NULL
    if action == 'download' :
        in_coins = NULL
        out_coins = NULL
        timestamp = 1515846393.1849742
        action = 'download'
        seller = 'zpf_uuid'
        buyer = 'buaa_uuid'
        data_uuid = 'mydata_uuid'
        credit = NULL
        reviewer = NULL
    if action == 'login' : # [默认为buyer 登录]
        in_coins = NULL
        out_coins = NULL
        timestamp = 1515846393.1849742
        action = 'login'
        # seller = 'zpf_uuid'
        buyer = 'buaa_uuid'
        data_uuid = NULL
        credit = NULL
        reviewer = NULL
    if action == 'review_pass' : # [管理员审核通过]
        in_coins = []
        out_coins = []
        timestamp = 1515846393.1849742
        action = 'review_pass'
        seller = 'zpf_uuid'
        buyer = ''
        data_uuid = 'mydata_uuid'
        credit = 0.0
        reviewer = 'admin_uuid'
    if action == 'review_reject' : # [管理员审核不通过]
        in_coins = []
        out_coins = []
        timestamp = 1515846393.1849742
        action = 'review_reject'
        seller = 'zpf_uuid'
        buyer = ''
        data_uuid = 'mydata_uuid'
        credit = 0.0
        reviewer = 'admin_uuid'
    if action == 'recharge' :
        in_coins = NULL
        out_coins = {
            coin_uuid: generate_uuid_coin,
            number_coin: credit( equals to credit)
            owner: seller ('zpf_uuid')
        }
        timestamp = 1515846393.1849742
        action = 'recharge'
        seller = 'zpf_uuid'
        buyer = NULL
        reviewer = NULL
        data_uuid = 'mydata_uuid'
        credit = 100.0
    """
    # later can change into more flexible
    def valid_transaction(self):
        assert self.action is not None, ('action should not be None')
        assert self.timestamp is not None, ('timestamp should not be None')

        if self.action == 'upload':
            assert len(self.in_coins) ==0 , ('Upload data, in_coins should be None, in_coins:', self.in_coins)
            assert len(self.out_coins) > 0 , ('Upload data, out_coins should not be None, out_coins:', self.out_coins)
            number_coin_total = 0.0
            for idx in range(len(self.out_coins)):
                assert self.out_coins[idx].owner == self.seller, (
                'Upload data, out_coins owner:', self.out_coins[idx].owner, 'seller:', self.seller)
                number_coin_total += self.out_coins[idx].number_coin
            assert number_coin_total == self.credit, (
            'Upload data, out_coins number_coin:', number_coin_total, 'credit:', self.credit)
            assert self.buyer is '', ('Upload data, buyer should be None, buyer:',self.buyer)
            assert self.seller is not '', ('Upload data, seller should not be None')
            assert self.data_uuid is not '', ('Upload data, data_uuid should not be None, data_uuid:', self.data_uuid)
            # assert self.credit is not None, ('Upload data, credit should be None, credit:',self.credit)
            assert self.credit >=0, ('Upload data, should have (+) credit reward. credit:',self.credit)
            assert self.reviewer is '', ('Upload data, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'buy':
            assert len(self.in_coins) > 0 , ('Buy data, in_coins should not be None, in_coins:', self.in_coins)
            assert len(self.out_coins) > 0 , ('Buy data, out_coins should not be None, out_coins:', self.out_coins)
            assert self.buyer is not '', ('Buy data, buyer should not be None, buyer:', self.buyer)
            assert self.seller is not '', ('Buy data, seller should not be None, seller:',self.seller)
            assert self.data_uuid is not '', ('Upload data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit is not '', ('Buy data, credit should be None, credit:', self.credit)
            assert self.credit >= 0, ('Buy data, should have (+) credit reward. credit:', self.credit)
            assert self.reviewer is '', ('Buy data, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'login':
            assert len(self.in_coins) == 0 , ('Login, in_coins should be None, in_coins:', self.in_coins)
            assert len(self.out_coins) == 0 , ('Login, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is '', ('Login, buyer should be None, buyer:', self.buyer)
            assert self.seller is not '', ('Login, seller should not be None, seller:', self.seller)
            assert self.data_uuid is '', ('Login, data_uuid should be None, data_uuid:', self.data_uuid)
            assert self.credit == 0.0, ('Login, credit should be None, credit:', self.credit)
            assert self.reviewer is '', ('Login, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'logout':
            assert len(self.in_coins) == 0 , ('Logout, in_coins should be None, in_coins:', self.in_coins)
            assert len(self.out_coins) == 0 , ('Logout, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is '', ('Logout, buyer should be None, buyer:', self.buyer)
            assert self.seller is not '', ('Logout, seller should not be None, seller:', self.seller)
            assert self.data_uuid is '', ('Logout, data_uuid should be None, data_uuid:', self.data_uuid)
            assert self.credit == 0.0, ('Logout, credit should be None, credit:', self.credit)
            assert self.reviewer is '', ('Logout, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'download':
            assert len(self.in_coins) == 0 , ('Download data, in_coins should be None, in_coins:', self.in_coins)
            assert len(self.out_coins) == 0 , ('Download data, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is '', ('Download data, buyer should be None, buyer:', self.buyer)
            assert self.seller is not '', ('Download data, seller should not be None, seller:', self.seller)
            assert self.data_uuid is not '', ('Download data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit == 0.0, ('Download data, credit should be None, credit:', self.credit)
            assert self.reviewer is '', ('Download data, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'review_pass':
            assert len(self.in_coins)==0, ('Review_pass data, in_coins should be None, in_coins:', self.in_coins)
            assert len(self.out_coins)==0, ('Review_pass data, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is '', ('Review_pass data, buyer should be None, buyer:', self.buyer)
            assert self.seller is not '', ('Review_pass data, seller should not be None, seller:', self.seller)
            assert self.data_uuid is not '', ('Review_pass data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit == 0.0, ('Review_pass data, credit should be None, credit:', self.credit)
            assert self.reviewer is not '', ('Review_pass data, reviewer should not be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'review_reject':
            assert len(self.in_coins)==0 , ('Review_reject data, in_coins should be None, in_coins:', self.in_coins)
            assert len(self.out_coins)==0, ('Review_reject data, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is '', ('Review_reject data, buyer should be None, buyer:', self.buyer)
            assert self.seller is not '', ('Review_reject data, seller should not be None, seller:', self.seller)
            assert self.data_uuid is not '', ('Review_reject data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit == 0.0, ('Review_reject data, credit should be None, credit:', self.credit)
            assert self.reviewer is not '', ('Review_reject data, reviewer should not be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'reset_pwd':
            assert len(self.in_coins) == 0 , ('Reset_pwd, in_coins should be None, in_coins:', self.in_coins)
            assert len(self.out_coins) == 0, ('Reset_pwd, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is '', ('Reset_pwd, buyer should be None, buyer:', self.buyer)
            assert self.seller is not '', ('Reset_pwd, seller should not be None, seller:', self.seller)
            assert self.data_uuid is not '', ('Reset_pwd, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit >= 0, ('Reset_pwd, credit should not be None, credit:', self.credit)
            assert self.reviewer is '', ('Reset_pwd, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'modify_pwd':
            assert len(self.in_coins) == 0 , ('Modify_pwd, in_coins should be None, in_coins:', self.in_coins)
            assert len(self.out_coins) == 0 , ('Modify_pwd, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is '', ('Modify_pwd, buyer should be None, buyer:', self.buyer)
            assert self.seller is not '', ('Modify_pwd, seller should not be None, seller:', self.seller)
            assert self.data_uuid is '', ('Modify_pwd, data_uuid should be None, data_uuid:', self.data_uuid)
            assert self.credit == 0.0, ('Modify_pwd, credit should be None, credit:', self.credit)
            assert self.reviewer is '', ('Modify_pwd, reviewer should be None, reviewer:', self.reviewer)
            return True
        else:
            pass
