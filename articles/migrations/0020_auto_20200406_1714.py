# Generated by Django 3.0.1 on 2020-04-06 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_auto_20200402_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articleId',
            field=models.CharField(default=datetime.datetime(2020, 4, 6, 17, 14, 31, 958326), max_length=255, primary_key=True, serialize=False),
        ),
    ]