# -*- coding: utf-8 -*-
# @Time    : 06/01/2018 1:16 PM
# @Author  : 伊甸一点
# @FileName: node.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

# TODO: here should be the node in network
from urllib.parse import urlparse

class Node:
    def __init__(self):
        self.node = set()
        pass

    def __eq__(self, other):
        pass

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.node = parsed_url.netloc