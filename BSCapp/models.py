from __future__ import unicode_literals
from django.db import models

from django.contrib import admin

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=64, primary_key=True)
    user_name = models.CharField(max_length=20, unique=True)
    user_pwd = models.CharField(max_length=20)
    user_email = models.EmailField()


class UserInfo(models.Model):
    user_id = models.CharField(max_length=64, primary_key=True)
    user_realName = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=20)
    user_idcard = models.CharField(max_length=20)
    user_company = models.CharField(max_length=20)
    user_title = models.CharField(max_length=20)
    user_place = models.CharField(max_length=20)


class Data(models.Model):
    data_id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64)
    data_name = models.CharField(max_length=64)
    data_info = models.CharField(max_length=200)
    timestamp = models.CharField(max_length=32)
    data_source = models.CharField(max_length=20)
    data_type = models.CharField(max_length=20)
    data_tag  = models.CharField(max_length=100)
    data_address = models.CharField(max_length=200)
    data_status = models.CharField(max_length=20)


class Transcation(models.Model):
    transaction_id = models.CharField(max_length=64, primary_key=True)
    buyer_id = models.CharField(max_length=64)
    seller_id = models.CharField(max_length=64)
    data_id = models.CharField(max_length=64)
    timestamp = models.CharField(max_length=32)
    price = models.FloatField()


class Coin(models.Model):
    coin_id = models.CharField(max_length=64, primary_key=True)
    owner_id = models.CharField(max_length=64)
    is_spent = models.BooleanField(default=False)
    timestamp = models.CharField(max_length=32)


class Recharge(models.Model):
    recharge_id = models.CharField(max_length=64, primary_key=True)
    user_id =  models.CharField(max_length=64)
    timestamp = models.CharField(max_length=32)
    credits = models.FloatField()
    before_account = models.FloatField()
    after_account = models.FloatField()
    coin_id = models.CharField(max_length=64)


class Wallet(models.Model):
    user_id = models.CharField(max_length=64, primary_key=True)
    account = models.FloatField()


class Download(models.Model):
    user_id = models.CharField(max_length=64)
    data_id = models.CharField(max_length=64)
    class Meta:
        unique_together=("user_id","data_id")


class Admin(models.Model):
    admin_id = models.CharField(max_length=64, primary_key=True)
    admin_name = models.CharField(max_length=20)
    admin_pwd = models.CharField(max_length=20)


class Review(models.Model):
    reviewer_id = models.CharField(max_length=64, primary_key=True)
    data_id = models.CharField(max_length=64)
    review_status = models.CharField(max_length=32)


class Notice(models.Model):
    notice_id = models.CharField(max_length=64,primary_key=True)
    user_id = models.CharField(max_length=64)
    notice_info = models.CharField(max_length=200)
    if_check = models.BooleanField(default=False)

