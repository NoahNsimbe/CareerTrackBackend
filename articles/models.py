from datetime import datetime
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    articleId = models.CharField(max_length=255, primary_key=True, default=datetime.now())

