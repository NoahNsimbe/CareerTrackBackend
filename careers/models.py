from django.db import models
from datetime import datetime


class Careers(models.Model):
    name = models.CharField(max_length=255, primary_key=True, default=datetime.now())
    description = models.CharField(max_length=255, default=datetime.now())
    courses = models.CharField(max_length=255, default=datetime.now())