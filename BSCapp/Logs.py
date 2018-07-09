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
        self.conference_data = []
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
            'conference_data': self.conference_data,
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
                science_data=None, conference_data=None, journal_data=None, patent_data=None, action=None, reviewer=None):
        self.tx_id = tx_id
        self.user_id = user_id
        self.timestamp = timestamp
        self.science_data = science_data
        self.conference_data = conference_data
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
        log.conference_data = log_json['conference_data']
        log.journal_data = log_json['journal_data']
        log.patent_data = log_json['patent_data']
        log.action = log_json['action']
        log.reviewer = log_json['reviewer']
        return log
