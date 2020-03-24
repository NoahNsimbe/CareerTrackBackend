from django.db import models
from datetime import datetime


class UaceSubjects(models.Model):
    code = models.CharField(max_length=255, primary_key=True,  default=datetime.now())
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default="optional")


class UceSubjects(models.Model):
    code = models.CharField(max_length=255, primary_key=True, default=datetime.now())
    name = models.CharField(max_length=255)



