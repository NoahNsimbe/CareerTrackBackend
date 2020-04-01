from django.contrib import admin
from .models import UaceSubjects, UceSubjects
models = [UaceSubjects, UceSubjects]
admin.site.register(models)
