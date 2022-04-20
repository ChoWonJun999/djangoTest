from django.db import models

# Create your models here.
class Test(models.Model):
    test_text = models.CharField(max_length=100)

class Status(models.Model):
    status_chk = models.BooleanField()