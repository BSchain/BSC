from __future__ import unicode_literals
from django.db import models

from django.contrib import admin

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=64, primary_key=True) # 用户id  generate_uuid  uuid5(SCOPE, name+time())
    user_name = models.CharField(max_length=20, unique=True) # 用户登录名
    user_pwd = models.CharField(max_length=20) #用户密码
    user_email = models.EmailField() # 用户邮箱
    user_realName = models.CharField(max_length=20) # 用户真实姓名
    user_phone = models.CharField(max_length=20) # 用户手机号
    user_idcard = models.CharField(max_length=20) # 用户身份证号
    user_company = models.CharField(max_length=64) # 用户所在公司
    user_title = models.CharField(max_length=20) # 用户职称
    user_addr = models.CharField(max_length=64, default='China') # 用户居住地

class Data(models.Model):
    data_id = models.CharField(max_length=64, primary_key=True) # 数据id
    user_id = models.CharField(max_length=64) # 用户id
    data_name = models.CharField(max_length=64) # 数据名称，由上传者定
    data_info = models.CharField(max_length=200) # 数据简介
    timestamp = models.CharField(max_length=32) # 时间戳
    data_source = models.CharField(max_length=20) # 数据来源 清华，北大，北航
    data_type = models.CharField(max_length=20) # 数据类型， csv, doc, mp3
    data_tag  = models.CharField(max_length=100) # 数据tag, 教育，医疗
    data_status = models.IntegerField(default=0) # status = 0 审核中. =1 审核通过 =2 审核不通过
    data_md5 = models.CharField(max_length=64) # 数据md5值，用于校验
    data_size = models.FloatField() # 数据大小
    data_download = models.IntegerField(default=0) # 数据下载量
    data_purchase = models.IntegerField(default=0) # 数据购买量
    data_price = models.FloatField() # 数据价格，信用度
    data_address = models.CharField(max_length=200)  # 数据保存在服务器地址url
    data_score = models.FloatField(default=0.0) # 数据平均评分结果 默认为0表示未评分
    comment_number = models.IntegerField(default=0) # 数据评价人数 默认没有人评价

class Income(models.Model):
    data_id = models.CharField(max_length=64)  # 数据id
    user_name = models.CharField(max_length=20)  # 用户登录名
    ratio = models.FloatField() # 该用户对此数据的收益占比
    class Meta:
        unique_together=("data_id","user_name") # 联合主键

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=64, primary_key=True) # 交易id
    buyer_id = models.CharField(max_length=64) # 购买者id
    seller_id = models.CharField(max_length=64) # 出售者id
    data_id = models.CharField(max_length=64) # 数据id
    timestamp = models.CharField(max_length=32)  #交易时间戳
    price = models.FloatField() # 成交价格, 信用度
    data_score = models.IntegerField(default=0) # 数据评分 1~5 默认为0表示未评价
    data_comment = models.CharField(max_length=200,default="") # 当前交易对数据的评价 默认评价为空 useless
    last_download_time = models.CharField(max_length=32, default="") # 上次下载数据时间 defalut = "" 表示未下载


class Coin(models.Model):
    coin_id = models.CharField(max_length=64, primary_key=True) # coin id
    owner_id = models.CharField(max_length=64) # 所有者id
    is_spent = models.BooleanField(default=False) # 当前coin 默认未花费
    timestamp = models.CharField(max_length=32) # coin生成时间
    coin_credit = models.FloatField() # 当前coin的价值


class Recharge(models.Model):
    recharge_id = models.CharField(max_length=64, primary_key=True) # 充值id
    user_id =  models.CharField(max_length=64) # 用户id
    timestamp = models.CharField(max_length=32) # 时间戳
    credits = models.FloatField() # 充值信用度
    before_account = models.FloatField() # 充值前账户信用度余额
    after_account = models.FloatField() # 充值后信用度余额
    coin_id = models.CharField(max_length=64) # 此次充值生成的coin id


class Wallet(models.Model):
    user_id = models.CharField(max_length=64, primary_key=True) # 用户id
    account = models.FloatField() # 账户余额 [仅用作展示，实际需要遍历区块链]


class Purchase(models.Model):
    user_id = models.CharField(max_length=64) # 用户id
    data_id = models.CharField(max_length=64) # 数据id
    class Meta:
        unique_together=("user_id","data_id") # 联合主键


class Admin(models.Model):
    admin_id = models.CharField(max_length=64, primary_key=True) # 管理员id
    admin_name = models.CharField(max_length=20) # 管理员登录名
    admin_pwd = models.CharField(max_length=20) # 管理员密码


class Review(models.Model):
    reviewer_id = models.CharField(max_length=64) # 审查者id
    data_id = models.CharField(max_length=64) # 所审核数据id
    review_status = models.IntegerField() # 数据状态 status = 0待审核 | 1 审核通过| 2 审核不通过
    timestamp = models.CharField(max_length=32) # 数据审核时间
    class Meta:
        unique_together=("reviewer_id","data_id") # 联合主键

class Notice(models.Model):
    notice_id = models.CharField(max_length=64,primary_key=True) # 通知信息id
    sender_id = models.CharField(max_length=64) # 信息发送方id (系统id 设置为generate_uuid(SCOPE, name='system'+time()))
    receiver_id = models.CharField(max_length=64)  # 信息接收方id
    notice_type = models.IntegerField() # 信息类型 ( 1: 数据审核通过信息，  2: 数据审核不通过信息， 3: 用户充值成功信息， 4:系统信息 )
    notice_info = models.CharField(max_length=200) # 通知信息内容 (sender_name + '在'+time() + switch notice_type: (different_notices)  需要提前进行构造)
    if_check = models.BooleanField(default=False) # 用户是否查看信息
    timestamp = models.CharField(max_length=32) # 此通知信息生成的时间

class Block(models.Model):
    height = models.IntegerField() # 保存区块高度 唯一
    timestamp = models.CharField(max_length=32) # 当前区块生成的时间
    block_size = models.FloatField() # 当前区块的大小
    tx_number = models.IntegerField() # 当前区块中保存的transaction数量
    block_hash = models.CharField(max_length=64) # 当前区块自身hash