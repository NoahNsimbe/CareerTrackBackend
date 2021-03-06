# Generated by Django 3.0.5 on 2020-11-11 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Careers',
            fields=[
                ('name', models.CharField(default='Provide career name', max_length=255, primary_key=True, serialize=False)),
                ('description', models.CharField(default='Provide career description', max_length=255)),
            ],
            options={
                'verbose_name': 'Careers and their description',
                'verbose_name_plural': 'Careers and their description',
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('code', models.CharField(default='Provide course code', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Provide course name', max_length=255)),
                ('description', models.CharField(default='Provide course description', max_length=255)),
                ('university', models.CharField(default='Provide university', max_length=255)),
                ('college', models.CharField(default='Provide college', max_length=255)),
                ('duration', models.IntegerField(default=3)),
                ('time', models.CharField(default='Day', max_length=255)),
            ],
            options={
                'verbose_name': 'Courses and their details',
                'verbose_name_plural': 'Courses and their details',
            },
        ),
        migrations.CreateModel(
            name='UaceSubjects',
            fields=[
                ('code', models.CharField(default="Subject code begins with 'UACE_'", max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Science', 'Science Subject'), ('Art', 'Art Subject'), ('Subsidiary', 'Subsidiary Subject'), ('Category', 'Category placeholder')], default='Art', max_length=15)),
                ('language_subject', models.BooleanField(default=False)),
                ('general_subject', models.BooleanField(default=False)),
                ('abbr', models.CharField(default='XX', max_length=255)),
            ],
            options={
                'verbose_name': 'Uace Subjects',
                'verbose_name_plural': 'Uace Subjects',
            },
        ),
        migrations.CreateModel(
            name='UceSubjects',
            fields=[
                ('code', models.CharField(default='Subject code begin with UCE_', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Compulsory', 'Compulsory Subject'), ('Elective', 'Elective Subject')], default='Elective', max_length=15)),
            ],
            options={
                'verbose_name': 'Uce Subjects',
                'verbose_name_plural': 'Uce Subjects',
            },
        ),
        migrations.CreateModel(
            name='OLevelConstraints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandatory', models.BooleanField(default=True)),
                ('maximum_grade', models.IntegerField(default=6)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Courses')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UceSubjects')),
            ],
            options={
                'verbose_name': 'O level constraints',
                'verbose_name_plural': 'O level constraints',
            },
        ),
        migrations.CreateModel(
            name='CutOffPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField(default=2019)),
                ('points', models.FloatField(default=0.0)),
                ('type', models.CharField(choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public')], default='PRIVATE', max_length=15)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Courses')),
            ],
            options={
                'verbose_name': 'Cut-off points',
                'verbose_name_plural': 'Cut-off points',
            },
        ),
        migrations.CreateModel(
            name='CourseSubjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compulsory_state', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('essential', 'essential'), ('relevant', 'relevant'), ('desirable', 'desirable')], default='essential', max_length=15)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Courses')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UaceSubjects')),
            ],
            options={
                'verbose_name': 'Course subjects',
                'verbose_name_plural': 'Course subjects',
            },
        ),
        migrations.CreateModel(
            name='CourseConstraints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('essentials', models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'One or Two')], default=2)),
                ('relevant', models.IntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'One or Two')], default=1)),
                ('desirable_state', models.IntegerField(choices=[(1, 'One Mandatory'), (2, 'Depends')], default=1)),
                ('a_level_constraint', models.BooleanField(default=False)),
                ('o_level_constraint', models.BooleanField(default=False)),
                ('all_subjects', models.BooleanField(default=False)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Courses')),
            ],
            options={
                'verbose_name': 'Course constraints',
                'verbose_name_plural': 'Course constraints',
            },
        ),
        migrations.CreateModel(
            name='CareerCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('career', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Careers')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Courses')),
            ],
            options={
                'verbose_name': 'Careers and respective courses',
                'verbose_name_plural': 'Careers and respective courses',
            },
        ),
        migrations.CreateModel(
            name='ALevelConstraints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_grade', models.IntegerField(default=2)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Courses')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UaceSubjects')),
            ],
            options={
                'verbose_name': 'A level constraints',
                'verbose_name_plural': 'A level constraints',
            },
        ),
    ]
