# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:11 PM
# @Author  : 伊甸一点
# @FileName: transaction.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

class Transaction:
    def __init__(self):
        self.in_coins = None
        self.out_coins = None
        self.timestamp = None
        self.action = None
        self.seller = None
        self.buyer = None
        self.data_uuid = None
        self.credit = None
        self.reviewer = None

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
        # FIXME: change to different kinds of structure
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
        self.in_coins.append(in_coins)
        self.out_coins.append(out_coins)
        self.timestamp = timestamp
        self.action = action
        self.seller = seller
        self.buyer = buyer
        self.data_uuid = data_uuid
        self.credit = credit
        self.reviewer = reviewer

    """

    卖数据seller = 'zpf_uuid'
    数据uuid = 'mydata_uuid'
    数据信用价格credit = 2.0
    时间戳timestamp = 1515846393.1849742
    买数据buyer = 'buaa_uuid'
    管理员reviewer = 'admin_uuid'

    if action == 'upload' :
        in_coins = NULL
        out_coins = [{
            coin_uuid: generate_uuid_coin, 
            number_coin: credit( equals to credit) 
            owner: seller ('zpf_uuid')  
        }]
        timestamp = 1515846393.1849742
        action = 'upload'
        seller = 'zpf_uuid'
        buyer = NULL 
        data_uuid = 'mydata_uuid'
        credit = 2.0

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
        in_coins = NULL
        out_coins = NULL
        timestamp = 1515846393.1849742
        action = 'review_pass'
        seller = 'zpf_uuid'
        buyer = NULL
        data_uuid = 'mydata_uuid'
        credit = NULL
        reviewer = 'admin_uuid'
    if action == 'review_reject' : # [管理员审核不通过]
        in_coins = NULL
        out_coins = NULL
        timestamp = 1515846393.1849742
        action = 'review_reject'
        seller = 'zpf_uuid'
        buyer = NULL
        data_uuid = 'mydata_uuid'
        credit = NULL
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
    # FIXME: later can change into more flexible
    def valid_transaction(self):
        assert self.action is not None, ('action should not be None')
        assert self.timestamp is not None, ('timestamp should not be None')

        if self.action == 'upload':
            assert self.in_coins is None, ('Upload data, in_coins should be None, in_coins:', self.in_coins)
            assert self.out_coins is not None, ('Upload data, out_coins should not be None, out_coins:', self.out_coins)
            number_coin_total = 0.0
            for idx in range(len(self.out_coins)):
                assert self.out_coins[idx].owner == self.seller, (
                'Upload data, out_coins owner:', self.out_coins[idx].owner, 'seller:', self.seller)
                number_coin_total += self.out_coins[idx].number_coin
            assert number_coin_total == self.credit, (
            'Upload data, out_coins number_coin:', number_coin_total, 'credit:', self.credit)
            assert self.buyer is None, ('Upload data, buyer should be None, buyer:',self.buyer)
            assert self.seller is not None, ('Upload data, seller should not be None')
            assert self.data_uuid is not None, ('Upload data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit is not None, ('Upload data, credit should be None, credit:',self.credit)
            assert self.credit >=0, ('Upload data, should have (+) credit reward. credit:',self.credit)
            assert self.reviewer is None, ('Upload data, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'buy': #TODO: need to fix those logist
            assert self.in_coins is not None, ('Buy data, in_coins should not be None, in_coins:', self.in_coins)
            assert self.out_coins is not None, ('Buy data, out_coins should not be None, out_coins:', self.out_coins)
            assert self.buyer is not None, ('Buy data, buyer should not be None, buyer:', self.buyer)
            assert self.seller is not None, ('Buy data, seller should not be None, seller:',self.seller)
            assert self.data_uuid is not None, ('Upload data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit is not None, ('Buy data, credit should be None, credit:', self.credit)
            assert self.credit >= 0, ('Buy data, should have (+) credit reward. credit:', self.credit)
            assert self.reviewer is None, ('Buy data, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'login':
            assert self.in_coins is None, ('Login, in_coins should be None, in_coins:', self.in_coins)
            assert self.out_coins is None, ('Login, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is None, ('Login, buyer should be None, buyer:', self.buyer)
            assert self.seller is not None, ('Login, seller should not be None, seller:', self.seller)
            assert self.data_uuid is None, ('Login, data_uuid should be None, data_uuid:', self.data_uuid)
            assert self.credit is None, ('Login, credit should be None, credit:', self.credit)
            assert self.reviewer is None, ('Login, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'download':
            assert self.in_coins is None, ('Download data, in_coins should be None, in_coins:', self.in_coins)
            assert self.out_coins is None, ('Download data, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is None, ('Download data, buyer should be None, buyer:', self.buyer)
            assert self.seller is not None, ('Download data, seller should not be None, seller:', self.seller)
            assert self.data_uuid is not None, ('Download data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit is None, ('Download data, credit should be None, credit:', self.credit)
            assert self.reviewer is None, ('Download data, reviewer should be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'review_pass':
            assert self.in_coins is None, ('Review_pass data, in_coins should be None, in_coins:', self.in_coins)
            assert self.out_coins is None, ('Review_pass data, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is None, ('Review_pass data, buyer should be None, buyer:', self.buyer)
            assert self.seller is not None, ('Review_pass data, seller should not be None, seller:', self.seller)
            assert self.data_uuid is not None, ('Review_pass data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit is None, ('Review_pass data, credit should be None, credit:', self.credit)
            assert self.reviewer is not None, ('Review_pass data, reviewer should not be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'review_reject':
            assert self.in_coins is None, ('Review_reject data, in_coins should be None, in_coins:', self.in_coins)
            assert self.out_coins is None, ('Review_reject data, out_coins should be None, out_coins:', self.out_coins)
            assert self.buyer is None, ('Review_reject data, buyer should be None, buyer:', self.buyer)
            assert self.seller is not None, ('Review_reject data, seller should not be None, seller:', self.seller)
            assert self.data_uuid is not None, ('Review_reject data, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit is None, ('Review_reject data, credit should be None, credit:', self.credit)
            assert self.reviewer is not None, ('Review_reject data, reviewer should not be None, reviewer:', self.reviewer)
            return True
        elif self.action == 'recharge':
            assert self.in_coins is None, ('Recharge, in_coins should be None, in_coins:', self.in_coins)
            assert self.out_coins is not None, ('Recharge, out_coins should not be None, out_coins:', self.out_coins)
            assert self.buyer is None, ('Recharge, buyer should be None, buyer:', self.buyer)
            assert self.seller is not None, ('Recharge, seller should not be None, seller:', self.seller)
            assert self.data_uuid is not None, ('Recharge, data_uuid should not be None, data_uuid:', self.data_uuid)
            assert self.credit is not None, ('Recharge, credit should not be None, credit:', self.credit)
            assert self.reviewer is None, ('Recharge, reviewer should be None, reviewer:', self.reviewer)
            return True
        else:
            pass
