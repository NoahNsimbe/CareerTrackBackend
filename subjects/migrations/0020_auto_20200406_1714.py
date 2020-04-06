# Generated by Django 3.0.1 on 2020-04-06 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0019_auto_20200404_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='uacesubjects',
            name='general_subject',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='uacesubjects',
            name='code',
            field=models.CharField(default="Subject code begins with 'UACE_'", max_length=255, primary_key=True, serialize=False),
        ),
    ]
