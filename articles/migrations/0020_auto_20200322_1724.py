# Generated by Django 3.0.1 on 2020-03-22 17:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_auto_20200322_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articleId',
            field=models.CharField(default=datetime.datetime(2020, 3, 22, 17, 24, 23, 108941), max_length=255, primary_key=True, serialize=False),
        ),
    ]
