# Generated by Django 3.0.1 on 2020-04-01 14:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20200401_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articleId',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 49, 1, 379380), max_length=255, primary_key=True, serialize=False),
        ),
    ]
