# Generated by Django 3.0.1 on 2020-04-02 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0025_auto_20200402_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseconstraints',
            name='relevant',
            field=models.IntegerField(choices=[(1, 'One'), (2, 'Two')], default=2),
        ),
    ]