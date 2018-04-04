# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-04 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_rec', models.DateField(auto_now=True)),
                ('topic', models.CharField(blank=True, default='mail topic', max_length=100)),
                ('body', models.TextField(default='It is message body.')),
                ('sender', models.CharField(default='mr. sender', max_length=100)),
                ('receiver', models.CharField(default='mr. receiver', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('department', models.IntegerField()),
            ],
        ),
    ]
