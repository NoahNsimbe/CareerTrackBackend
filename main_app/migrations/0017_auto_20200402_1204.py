# Generated by Django 3.0.1 on 2020-04-02 12:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_auto_20200401_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careers',
            name='description',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 392903), max_length=255),
        ),
        migrations.AlterField(
            model_name='careers',
            name='name',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 392865), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courses',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 393296), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courses',
            name='college',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 393407), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='description',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 393358), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='duration',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 393436), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='name',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 393331), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='time',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 393460), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='university',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 12, 4, 37, 393383), max_length=255),
        ),
    ]