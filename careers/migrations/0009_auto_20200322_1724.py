# Generated by Django 3.0.1 on 2020-03-22 17:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0008_auto_20200322_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careers',
            name='courses',
            field=models.CharField(default=datetime.datetime(2020, 3, 22, 17, 24, 44, 113580), max_length=255),
        ),
        migrations.AlterField(
            model_name='careers',
            name='description',
            field=models.CharField(default=datetime.datetime(2020, 3, 22, 17, 24, 44, 113553), max_length=255),
        ),
        migrations.AlterField(
            model_name='careers',
            name='name',
            field=models.CharField(default=datetime.datetime(2020, 3, 22, 17, 24, 44, 113516), max_length=255, primary_key=True, serialize=False),
        ),
    ]
