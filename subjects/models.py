from django.db import models
from datetime import datetime


class UaceSubjects(models.Model):
    code = models.CharField(max_length=255, primary_key=True,  default=datetime.now())
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default="Not specified", choices=(
        ("Science", "Science"), ("Art", "Art"), ("Subsidiary", "Subsidiary")))
    abbr = models.CharField(max_length=255, default='XX')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Uace Subjects'


class UceSubjects(models.Model):
    code = models.CharField(max_length=255, primary_key=True, default=datetime.now())
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Uce Subjects'



