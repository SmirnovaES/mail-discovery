from django.db import models
from datetime import datetime

# Create your models here.

class Letter(models.Model):
  date_rec = models.DateField(auto_now=True)
  topic = models.CharField(max_length=100, blank=True, default='mail topic')
  body = models.TextField(default='It is message body.')
  sender = models.CharField(default='mr. sender', max_length=100)
  receiver = models.CharField(default='mr. receiver', max_length=100)

class Person(models.Model):
  name = models.CharField(max_length=100, blank=True)
  department = models.IntegerField()

