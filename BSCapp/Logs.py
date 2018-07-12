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
        self.science_data_id_list = []
        self.conference_data_id_list = []
        self.journal_data_id_list = []
        self.patent_data_id_list = []
        self.action = ''
        self.reviewer = ''
        self.first_title = ''
        self.second_title = ''
        self.data_type = ''

    def to_dict(self):
        # change to different kinds of structure
        log = {
            'tx_id': self.tx_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
            'science_data_id_list': self.science_data_id_list,
            'conference_data_id_list': self.conference_data_id_list,
            'journal_data_id_list': self.journal_data_id_list,
            'patent_data_id_list': self.patent_data_id_list,
            'action': self.action,
            'reviewer': self.reviewer,
            'first_title': self.first_title,
            'second_title': self.second_title,
            'data_type': self.data_type,
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
                science_data_id_list=None, conference_data_id_list=None, journal_data_id_list=None, patent_data_id_list=None,
                action=None, reviewer=None, first_title= None, second_title= None, data_type=None):
        self.tx_id = tx_id
        self.user_id = user_id
        self.timestamp = timestamp
        self.science_data_id_list = science_data_id_list
        self.conference_data_id_list = conference_data_id_list
        self.journal_data_id_list = journal_data_id_list
        self.patent_data_id_list = patent_data_id_list
        self.action = action
        self.reviewer = reviewer
        self.first_title = first_title
        self.second_title = second_title
        self.data_type = data_type
    @staticmethod
    def json_to_log(log_json):
        log = Logs()
        log.tx_id = log_json['tx_id']
        log.user_id = log_json['user_id']
        log.timestamp = log_json['timestamp']
        log.science_data = log_json['science_data_id_list']
        log.conference_data = log_json['conference_data_id_list']
        log.journal_data = log_json['journal_data_id_list']
        log.patent_data = log_json['patent_data_id_list']
        log.action = log_json['action']
        log.reviewer = log_json['reviewer']
        log.reviewer = log_json['first_title']
        log.reviewer = log_json['second_title']
        log.reviewer = log_json['data_type']
        return log
