# Generated by Django 3.0.1 on 2020-03-22 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0024_auto_20200322_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articleId',
            field=models.CharField(default=datetime.datetime(2020, 3, 22, 19, 43, 5, 196459), max_length=255, primary_key=True, serialize=False),
        ),
    ]
