# Generated by Django 3.0.1 on 2020-04-05 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0026_auto_20200402_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseconstraints',
            name='relevant',
            field=models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'One or Two')], default=1),
        ),
    ]
