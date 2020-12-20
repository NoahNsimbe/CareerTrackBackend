import enum
from datetime import datetime
from ckeditor.fields import RichTextField
from django.db import models


def article_images_folder(instance, filename):
    folder = str(instance.title).replace(" ", "_")
    return 'articles/{0}/images/{1}'.format(folder, filename)


class Careers(models.Model):
    name = models.CharField(max_length=255, primary_key=True, default="Provide career name")
    description = models.CharField(max_length=255, default="Provide career description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Careers and their description'


class Articles(models.Model):

    author = models.CharField(max_length=50, default="Anonymous")
    author_image = models.ImageField(upload_to=article_images_folder, null=True, blank=True)
    author_image_alt = models.CharField(max_length=255, null=True, blank=True)

    title = models.CharField(max_length=255, null=True, blank=True)
    article_image = models.ImageField(upload_to=article_images_folder, null=True, blank=True)
    article_image_alt = models.CharField(max_length=255, null=True, blank=True)
    read_time = models.DurationField(help_text="<b><em>In seconds e.g. enter 60 for 1 minute</em></b>")
    bait = models.TextField(null=True, blank=True)
    body = RichTextField(null=True, blank=True)

    tags = models.CharField(max_length=50, null=True, blank=True)

    claps = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_on']

    def __str__(self):
        return str(self.title)


class Courses(models.Model):
    code = models.CharField(max_length=255, primary_key=True, default="Provide course code")
    name = models.CharField(max_length=255, default="Provide course name")
    description = models.CharField(max_length=255, default="Provide course description")
    university = models.CharField(max_length=255, default="Provide university")
    college = models.CharField(max_length=255, default="Provide college")
    duration = models.IntegerField(default=3)
    time = models.CharField(max_length=255, default="Day")

    def __str__(self):
        return str(self.name) + " (" + str(self.code) + ")"

    class Meta:
        verbose_name = verbose_name_plural = 'Courses and their details'


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

    code = models.CharField(max_length=255, primary_key=True, default="Subject code begins with 'UACE_'")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=15, choices=SUBJECT_CATEGORIES, default=ART)
    language_subject = models.BooleanField(default=False)
    general_subject = models.BooleanField(default=False)
    abbr = models.CharField(max_length=255, default='XX')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Uace Subjects'


class UceSubjects(models.Model):
    COMPULSORY = 'Compulsory'
    ELECTIVE = 'Elective'

    SUBJECT_CATEGORIES = [
        (COMPULSORY, 'Compulsory Subject'),
        (ELECTIVE, 'Elective Subject')
    ]

    code = models.CharField(max_length=255, primary_key=True, default="Subject code begin with UCE_")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=15, choices=SUBJECT_CATEGORIES, default=ELECTIVE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Uce Subjects'


class CareerCourses(models.Model):
    career = models.ForeignKey(Careers, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.career

    class Meta:
        verbose_name = verbose_name_plural = 'Careers and respective courses'


class CourseConstraints(models.Model):
    ONE_ESSENTIAL = 1
    TWO_ESSENTIALS = 2
    ONE_OR_TWO_ESSENTIALS = 3

    ONE_DESIRABLE = 1
    TWO_DESIRABLE = 2

    ONE_RELEVANT = 1
    TWO_RELEVANT = 2
    ONE_OR_TWO_RELEVANT = 3

    COURSE_ESSENTIALS_CHOICES = [
        (ONE_ESSENTIAL, "One"),
        (TWO_ESSENTIALS, "Two"),
        (ONE_OR_TWO_ESSENTIALS, "One or Two"),
    ]

    COURSE_DESIRABLE_CHOICES = [
        (ONE_DESIRABLE, "One Mandatory"),
        (TWO_DESIRABLE, "Depends"),
    ]

    COURSE_RELEVANT_CHOICES = [
        (ONE_RELEVANT, "One"),
        (TWO_RELEVANT, "Two"),
        (ONE_OR_TWO_RELEVANT, "One or Two"),
    ]

    course = models.OneToOneField(Courses, on_delete=models.CASCADE)

    essentials = models.IntegerField(
        choices=COURSE_ESSENTIALS_CHOICES,
        default=TWO_ESSENTIALS,
    )
    relevant = models.IntegerField(
        choices=COURSE_RELEVANT_CHOICES,
        default=ONE_RELEVANT,
    )
    desirable_state = models.IntegerField(
        choices=COURSE_DESIRABLE_CHOICES,
        default=ONE_DESIRABLE,
    )
    # subject_constraint = models.BooleanField(default=False)
    a_level_constraint = models.BooleanField(default=False)
    o_level_constraint = models.BooleanField(default=False)
    all_subjects = models.BooleanField(default=False)

    class Meta:
        verbose_name = verbose_name_plural = 'Course constraints'

    # def __str__(self):
    #     return str('%s object' % self.__class__.__name__)


class CourseSubjects(models.Model):
    ESSENTIAL = 'essential'
    RELEVANT = 'relevant'
    DESIRABLE = 'desirable'

    COURSE_CATEGORY_CHOICES = [
        (ESSENTIAL, 'essential'),
        (RELEVANT, 'relevant'),
        (DESIRABLE, 'desirable'),
    ]

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    subject = models.ForeignKey(UaceSubjects, on_delete=models.CASCADE)
    compulsory_state = models.BooleanField(default=False)
    category = models.CharField(max_length=15, choices=COURSE_CATEGORY_CHOICES, default=ESSENTIAL,)

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


class CutOffPoints(models.Model):
    PRIVATE = "PRIVATE"
    GOVT = "PUBLIC"

    MALE = "MALE"
    FEMALE = "FEMALE"
    BOTH = "BOTH"

    ADMISSION_TYPE = [(PRIVATE, "Private"), (GOVT, "Public")]

    GENDER = [(MALE, "Male"), (FEMALE, "Female"), (BOTH, "Both")]

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(default=datetime.now().year - 1)
    points = models.FloatField(default=0.0)
    type = models.CharField(max_length=15, choices=ADMISSION_TYPE, default=GOVT)
    gender = models.CharField(max_length=15, choices=GENDER, default=BOTH)

    class Meta:
        verbose_name = verbose_name_plural = 'Cut-off points'


class AppRequests(enum.Enum):

    UceProgram = "UceProgram"
    UceProgramResults = "UceProgramResults"

    UaceProgram = "UaceProgram"
    UaceProgramResults = "UaceProgramResults"
    UceCombination = "UceCombination"
