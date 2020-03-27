# Generated by Django 3.0.1 on 2020-03-26 20:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0019_auto_20200326_2014'),
        ('main_app', '0010_auto_20200322_1943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseconstraints',
            old_name='code',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='courseconstraints',
            old_name='no_of_essential',
            new_name='relevant',
        ),
        migrations.RemoveField(
            model_name='courseconstraints',
            name='no_of_relevant',
        ),
        migrations.AddField(
            model_name='courseconstraints',
            name='desirable_state',
            field=models.IntegerField(choices=[(1, 'Only one mandatory desirable'), (2, 'Depends on essential and relevant subjects')], default=1),
        ),
        migrations.AddField(
            model_name='courseconstraints',
            name='essentials',
            field=models.IntegerField(choices=[(1, 'One Essential'), (2, 'Two Essentials'), (3, 'One or two essentials')], default=2),
        ),
        migrations.AlterField(
            model_name='careers',
            name='description',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 559687), max_length=255),
        ),
        migrations.AlterField(
            model_name='careers',
            name='name',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 559647), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courses',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560030), max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='courses',
            name='college',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560144), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='description',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560093), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='desirable',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560251), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='duration',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560169), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='essential',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560194), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='name',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560066), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='relevant',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560217), max_length=255),
        ),
        migrations.AlterField(
            model_name='courses',
            name='university',
            field=models.CharField(default=datetime.datetime(2020, 3, 26, 20, 13, 30, 560119), max_length=255),
        ),
        migrations.CreateModel(
            name='OLevelConstraints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandatory', models.BooleanField(default=True)),
                ('maximum_grade', models.IntegerField(default=6)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Courses')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.UceSubjects')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSubjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('essential', 'essential'), ('relevant', 'relevant'), ('desirable', 'desirable')], max_length=15)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Courses')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.UaceSubjects')),
            ],
        ),
        migrations.CreateModel(
            name='ALevelConstraints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandatory', models.BooleanField(default=True)),
                ('minimum_grade', models.IntegerField(default=2)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Courses')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.UaceSubjects')),
            ],
        ),
    ]
