from django.db import models
from datetime import datetime


class Careers(models.Model):
    name = models.CharField(max_length=255)


