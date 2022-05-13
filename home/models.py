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

class User(models.Model) :
    """
        user

        Columns
        user_id     아이디
        user_pw     비밀번호
    """
    user_id = models.CharField(max_length=100)
    user_pw = models.CharField(max_length=100)
    access_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)