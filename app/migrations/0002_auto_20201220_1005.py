# Generated by Django 3.0.5 on 2020-12-20 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cutoffpoints',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('BOTH', 'Both')], default='BOTH', max_length=15),
        ),
        migrations.AlterField(
            model_name='cutoffpoints',
            name='type',
            field=models.CharField(choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public')], default='PUBLIC', max_length=15),
        ),
    ]