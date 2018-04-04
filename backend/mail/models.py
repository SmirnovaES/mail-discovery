from django.db import models
from datetime import datetime

# Create your models here.

class mails(models.Model):
  Date = models.DateTimeField(default=datetime.now, blank=True)
  NameFrom = models.CharField(max_length=100, blank=True)
  AddressFrom = models.CharField(max_length=100, blank=True)
  NameTo = models.CharField(max_length=100, blank=True)
  AddressTo = models.CharField(max_length=100, blank=True)
  Subject = models.CharField(max_length=100, blank=True)
  Message = models.TextField(blank=True)

class users(models.Model):
  Name = models.CharField(max_length=100, blank=True)
  Address = models.CharField(max_length=100, blank=True)
  DateBegin = models.DateTimeField(default=datetime.now, blank=True)
  DateEnd = models.DateTimeField(default=datetime.now, blank=True)
  Department = models.CharField(max_length=100, blank=True)


