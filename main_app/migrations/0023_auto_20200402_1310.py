# Generated by Django 3.0.1 on 2020-04-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_auto_20200402_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseconstraints',
            name='essentials',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3)], default=2, max_length=15),
        ),
    ]