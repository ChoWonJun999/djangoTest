from django.db import models

# Create your models here.
class Test(models.Model):
    test_text = models.CharField(max_length=100)

class Status(models.Model):
    """
    auto trade status

    Columns
    status_chk          1:off / 0:on
    trade_method_id     home_trade_method PK
    trade_method        방식
    """
    status_chk = models.BooleanField()
    trade_method_id = models.IntegerField()
    trade_method = models.CharField(max_length=100)

class Trade_method(models.Model):
    """
    auto trade method

    Columns
    method_name     방식
    method_text     방식 설명
    """
    method_name = models.CharField(max_length=100)
    method_text = models.TextField()

class Api_key(models.Model):
    """
    auto trade method

    Columns
    access_key      access_key
    secret_key      secret_key
    """
    access_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)