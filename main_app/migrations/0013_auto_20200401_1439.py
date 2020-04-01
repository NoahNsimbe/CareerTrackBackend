# Generated by Django 3.0.1 on 2020-04-01 14:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_auto_20200329_1227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alevelconstraints',
            options={'verbose_name': 'A level constraints', 'verbose_name_plural': 'A level constraints'},
        ),
        migrations.AlterModelOptions(
            name='careercourses',
            options={'verbose_name': 'Careers and respective courses', 'verbose_name_plural': 'Careers and respective courses'},
        ),
        migrations.AlterModelOptions(
            name='careers',
            options={'verbose_name': 'Careers and their description', 'verbose_name_plural': 'Careers and their description'},
        ),
        migrations.AlterModelOptions(
            name='courseconstraints',
            options={'verbose_name': 'Course constraints', 'verbose_name_plural': 'Course constraints'},
        ),
        migrations.AlterModelOptions(
            name='courses',
            options={'verbose_name': 'Courses and their details', 'verbose_name_plural': 'Courses and their details'},
        ),
        migrations.AlterModelOptions(
            name='coursesubjects',
            options={'verbose_name': 'Course subjects', 'verbose_name_plural': 'Course subjects'},
        ),
        migrations.AlterModelOptions(
            name='olevelconstraints',
            options={'verbose_name': 'O level constraints', 'verbose_name_plural': 'O level constraints'},
        ),
        migrations.AlterField(
            model_name='careers',
            name='description',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 689954), max_length=255),
        ),
        migrations.AlterField(
            model_name='careers',
            name='name',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 689915), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courses',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 690366), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courses',
            name='college',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 690478), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='description',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 690429), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='duration',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 690501), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='name',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 690401), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='time',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 690525), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='university',
            field=models.CharField(default=datetime.datetime(2020, 4, 1, 14, 39, 6, 690453), max_length=255),
        ),
    ]
