# Generated by Django 2.0.2 on 2018-04-04 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_auto_20180404_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='Department',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]