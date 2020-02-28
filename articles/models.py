from datetime import datetime
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    # articlePicture = models.BinaryField()
    body = models.CharField(max_length=255)
    # likes = models.IntegerField()
    # dislikes = models.IntegerField()
    # datePosted = models.DateTimeField()
    # author = models.CharField(max_length=255)
    articleId = models.CharField(max_length=255, primary_key=True, default=datetime.now())
    # articleLink = models.URLField()
