# Generated by Django 3.0.1 on 2020-03-08 14:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0002_auto_20200308_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careers',
            name='courses',
            field=models.CharField(default=datetime.datetime(2020, 3, 8, 14, 37, 48, 507826), max_length=255),
        ),
        migrations.AlterField(
            model_name='careers',
            name='description',
            field=models.CharField(default=datetime.datetime(2020, 3, 8, 14, 37, 48, 507798), max_length=255),
        ),
        migrations.AlterField(
            model_name='careers',
            name='name',
            field=models.CharField(default=datetime.datetime(2020, 3, 8, 14, 37, 48, 507760), max_length=255, primary_key=True, serialize=False),
        ),
    ]
