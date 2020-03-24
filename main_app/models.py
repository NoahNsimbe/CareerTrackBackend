from django.db import models
from datetime import datetime
from subjects.models import UceSubjects, UaceSubjects


class Careers(models.Model):
    name = models.CharField(max_length=255, primary_key=True, default=datetime.now())
    description = models.CharField(max_length=255, default=datetime.now())


class Courses(models.Model):
    code = models.CharField(max_length=255, primary_key=True, default=datetime.now())
    name = models.CharField(max_length=255, default=datetime.now())
    description = models.CharField(max_length=255, default=datetime.now())
    university = models.CharField(max_length=255, default=datetime.now())
    college = models.CharField(max_length=255, default=datetime.now())
    duration = models.CharField(max_length=255, default=datetime.now())
    essential = models.CharField(max_length=255, default=datetime.now())
    relevant = models.CharField(max_length=255, default=datetime.now())
    desirable = models.CharField(max_length=255, default=datetime.now())


class CareerCourses(models.Model):
    career = models.ForeignKey(Careers, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)


class CourseConstraints(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    essentials = models.IntegerField(default=2, choices=(
        (1, "One Essential"), (2, "Two Essentials"), (3, "One or two essentials"))
                                     )
    relevant = models.IntegerField(default=2)
    desirable_state = models.IntegerField(default=1, choices=(
        (1, "Only one mandatory desirable"), (2, "Depends on essential and relevant subjects"))
                                          )


class CourseSubjects(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject = models.ForeignKey(UaceSubjects, on_delete=models.CASCADE)
    category = models.CharField(max_length=15, choices=(
        ("essential", "essential"), ("relevant", "relevant"), ("desirable", "desirable"))
                                )


class ALevelConstraints(models.Model):
    code = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject = models.ForeignKey(UaceSubjects, on_delete=models.CASCADE)
    mandatory = models.BooleanField(default=True)
    minimum_grade = models.IntegerField(default=2)


class OLevelConstraints(models.Model):
    code = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject = models.ForeignKey(UceSubjects, on_delete=models.CASCADE)
    mandatory = models.BooleanField(default=True)
    maximum_grade = models.IntegerField(default=6)

