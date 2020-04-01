# Generated by Django 3.0.1 on 2020-04-01 14:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0003_auto_20200401_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uacesubjects',
            name='abbr',
            field=models.CharField(default='XX', max_length=255),
        ),
        migrations.AlterField(
            model_name='uacesubjects',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 40, 28, 868825), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ucesubjects',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 40, 28, 869445), max_length=255, primary_key=True, serialize=False),
        ),
    ]