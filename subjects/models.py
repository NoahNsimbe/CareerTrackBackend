from django.db import models


class UaceSubjects(models.Model):
    SCIENCE = 'Science'
    ART = 'Art'
    SUBSIDIARY = 'Subsidiary'
    NONE = 'Category'

    SUBJECT_CATEGORIES = [
        (SCIENCE, 'Science Subject'),
        (ART, 'Art Subject'),
        (SUBSIDIARY, 'Subsidiary Subject'),
        (NONE, 'Category placeholder'),
    ]

    code = models.CharField(max_length=255, primary_key=True,  default="Subject code begin with UACE_")
    name = models.CharField(max_length=255)
    category = models.CharField(
        max_length=15,
        choices=SUBJECT_CATEGORIES,
        default=ART,
    )
    language_subject = models.BooleanField(default=False)
    abbr = models.CharField(max_length=255, default='XX')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Uace Subjects'


class UceSubjects(models.Model):
    code = models.CharField(max_length=255, primary_key=True, default="Subject code begin with UCE_")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Uce Subjects'



