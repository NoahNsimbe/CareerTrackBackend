from django.db import models
from datetime import datetime


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
    code = models.ForeignKey(Courses, on_delete=models.CASCADE)
    no_of_essential = models.IntegerField(default=2)
    no_of_relevant = models.IntegerField(default=1)

