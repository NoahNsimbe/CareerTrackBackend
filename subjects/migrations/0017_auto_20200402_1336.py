# Generated by Django 3.0.1 on 2020-04-02 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0016_auto_20200402_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='uacesubjects',
            name='language_subject',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='uacesubjects',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 13, 36, 22, 717350), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ucesubjects',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 4, 2, 13, 36, 22, 718028), max_length=255, primary_key=True, serialize=False),
        ),
    ]