# -*- coding: utf-8 -*-
# @Time    : 07/01/2018 12:29 AM
# @Author  : 伊甸一点
# @FileName: coin.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

class Coin:
    def __init__(self):
        self.coin_uuid = None
        self.number_coin = None
        self.owner = None

    def new_coin(self, coin_uuid, number_coin, owner):
        """

        :param coin_uuid:
        :param number_coin:
        :param owner:
        :return:
        """
        self.coin_uuid = coin_uuid
        self.number_coin = number_coin
        self.owner = owner

    def to_dict(self):
        coin = {
            'coin_uuid': self.coin_uuid,
            'number_coin': self.number_coin,
            'owner': self.owner,
        }
        return coin

    def __eq__(self, other):
        return self.coin_uuid == other.coin_uuid and \
               self.number_coin == other.number_coin and \
               self.owner == other.owner

    def __ne__(self, other):
        return not self.__eq__(other)

