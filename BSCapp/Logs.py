# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 下午12:26
# @Author  : 伊甸一点
# @FileName: Logs.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

import os
from BSCapp.root_chain.utils import *

class Logs:
    def __init__(self):
        self.tx_id = ''
        self.user_id = ''
        self.timestamp = ''
        self.science_data = []
        self.conerence_data = []
        self.journal_data = []
        self.patent_data = []
        self.action = ''
        self.reviewer = ''

    def to_dict(self):
        # change to different kinds of structure
        log = {
            'tx_id': self.tx_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
            'science_data': self.science_data,
            'conerence_data': self.conerence_data,
            'journal_data': self.journal_data,
            'patent_data': self.patent_data,
            'action': self.action,
            'reviewer': self.reviewer,
        }
        return log

    def save_log(self):
        if os.path.exists(LOG_SAVE_ROOT) == False:
            os.mkdir(LOG_SAVE_ROOT)
        assert os.path.exists(LOG_SAVE_ROOT), (LOG_SAVE_ROOT,' not exist')
        save_tx_path = LOG_SAVE_ROOT + str(self.timestamp) + LOG_SAVE_SUFFIX
        with open(save_tx_path, 'w',encoding='utf-8') as json_file:
            json_file.write(json.dumps(self.to_dict()))

    def new_log(self, tx_id=None, user_id=None, timestamp=None,
                science_data=None, conerence_data=None, journal_data=None, patent_data=None, action=None, reviewer=None):
        self.tx_id = tx_id
        self.user_id = user_id
        self.timestamp = timestamp
        self.science_data = science_data
        self.conerence_data = conerence_data
        self.journal_data = journal_data
        self.patent_data = patent_data
        self.action = action
        self.reviewer = reviewer

    @staticmethod
    def json_to_log(log_json):
        log = Logs()
        log.tx_id = log_json['tx_id']
        log.user_id = log_json['user_id']
        log.timestamp = log_json['timestamp']
        log.science_data = log_json['science_data']
        log.conerence_data = log_json['conerence_data']
        log.journal_data = log_json['journal_data']
        log.patent_data = log_json['patent_data']
        log.action = log_json['action']
        log.reviewer = log_json['reviewer']
        return log

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
