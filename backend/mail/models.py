# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class mails(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    namefrom = models.TextField(blank=True, null=True)
    addressfrom = models.TextField(blank=True, null=True)
    nameto = models.TextField(blank=True, null=True)
    addressto = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mails'


class users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    datebegin = models.DateTimeField(blank=True, null=True)
    dateend = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
