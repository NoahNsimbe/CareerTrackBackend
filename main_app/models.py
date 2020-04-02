from django.db import models
from datetime import datetime
from subjects.models import UceSubjects, UaceSubjects


class Careers(models.Model):
    name = models.CharField(max_length=255, primary_key=True, default="Provide career name")
    description = models.CharField(max_length=255, default="Provide career description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Careers and their description'


class Courses(models.Model):
    code = models.CharField(max_length=255, primary_key=True, default="Provide course code")
    name = models.CharField(max_length=255, default="Provide course name")
    description = models.CharField(max_length=255, default="Provide course description")
    university = models.CharField(max_length=255, default="Provide university")
    college = models.CharField(max_length=255, default="Provide college")
    duration = models.IntegerField(default=3)
    time = models.CharField(max_length=255, default="Day")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Courses and their details'


class CareerCourses(models.Model):
    career = models.ForeignKey(Careers, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.career

    class Meta:
        verbose_name = verbose_name_plural = 'Careers and respective courses'


class CourseConstraints(models.Model):
    course = models.OneToOneField(Courses, on_delete=models.CASCADE)
    essentials = models.CharField(max_length=255, default=2, choices=(
        (1, "One Essential"), (2, "Two Essentials"), (3, "One or two essentials"))
                                     )
    relevant = models.CharField(max_length=255, default=2)
    desirable_state = models.CharField(max_length=255, default=1, choices=(
        (1, "Only one mandatory desirable"), (2, "Depends on essential and relevant subjects"))
                                          )
    subject_constraint = models.BooleanField(default=False)
    a_level_constraint = models.BooleanField(default=False)
    o_level_constraint = models.BooleanField(default=False)
    all_subjects = models.BooleanField(default=False)

    class Meta:
        verbose_name = verbose_name_plural = 'Course constraints'

    # def __str__(self):
    #     return str('%s object' % self.__class__.__name__)


class CourseSubjects(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject = models.ForeignKey(UaceSubjects, on_delete=models.CASCADE)
    category = models.CharField(max_length=15, choices=(
        ("essential", "essential"), ("relevant", "relevant"), ("desirable", "desirable"))
                                )
    compulsory_state = models.BooleanField(default=False)

    class Meta:
        verbose_name = verbose_name_plural = 'Course subjects'


class ALevelConstraints(models.Model):
    code = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject = models.ForeignKey(UaceSubjects, on_delete=models.CASCADE)
    minimum_grade = models.IntegerField(default=2)

    class Meta:
        verbose_name = verbose_name_plural = 'A level constraints'


class OLevelConstraints(models.Model):
    code = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject = models.ForeignKey(UceSubjects, on_delete=models.CASCADE)
    mandatory = models.BooleanField(default=True)
    maximum_grade = models.IntegerField(default=6)

    class Meta:
        verbose_name = verbose_name_plural = 'O level constraints'

