from django.contrib import admin
from .models import UaceSubjects, UceSubjects
# models = [UaceSubjects, UceSubjects]
# admin.site.register(models)


@admin.register(UaceSubjects)
class UaceSubjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'abbr', 'language_subject')
    ordering = ['name']
    search_fields = ['code', 'name']


@admin.register(UceSubjects)
class UceSubjectsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name']
    search_fields = ['code', 'name']