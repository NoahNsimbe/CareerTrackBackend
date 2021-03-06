from django.contrib import admin
from .models import Careers, Courses, CareerCourses, CourseConstraints, ALevelConstraints, CourseSubjects, \
    OLevelConstraints, CutOffPoints, UaceSubjects, UceSubjects, Articles


@admin.register(Careers)
class CareersAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ['name']
    search_fields = ('name', 'description')


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'updated_on', 'claps')
    ordering = ('-created_on',)
    group_by = ('author_name',)
    readonly_fields = ('claps', 'created_on', 'updated_on',)


@admin.register(CutOffPoints)
class CutOffPointsAdmin(admin.ModelAdmin):
    list_display = ('course', 'year', 'type', 'points', 'gender')
    ordering = ['year']
    search_fields = ('course', 'year')
    autocomplete_fields = ['course']


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'college')
    ordering = ['college']
    search_fields = ('name', 'code')


@admin.register(CareerCourses)
class CareerCoursesAdmin(admin.ModelAdmin):
    list_display = ('career', 'course')
    ordering = ['career']
    search_fields = ('career__name', 'career__description', 'course__code', 'course__name')
    autocomplete_fields = ['course', 'career']


@admin.register(CourseConstraints)
class CourseConstraintsAdmin(admin.ModelAdmin):
    list_display = ('course', 'essentials', 'relevant', 'desirable_state', 'a_level_constraint', 'all_subjects')
    ordering = ['course']
    search_fields = ['course__code', 'course__name']
    autocomplete_fields = ['course']


@admin.register(ALevelConstraints)
class ALevelConstraintsAdmin(admin.ModelAdmin):
    list_display = ('code', 'subject', 'minimum_grade')
    ordering = ['code']
    search_fields = ['code__code', 'code__name', 'subject__code']


@admin.register(CourseSubjects)
class CourseSubjectsAdmin(admin.ModelAdmin):
    list_display = ('course', 'subject', 'category', 'compulsory_state')
    ordering = ['course', 'category']
    search_fields = ['course__code', 'course__name']
    autocomplete_fields = ['course', 'subject']


@admin.register(OLevelConstraints)
class OLevelConstraintsAdmin(admin.ModelAdmin):
    list_display = ('code', 'subject', 'maximum_grade')
    ordering = ['code']
    search_fields = ['code__code', 'code__name', 'subject__code']


@admin.register(UaceSubjects)
class UaceSubjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'abbr', 'language_subject')
    ordering = ['name']
    search_fields = ['code', 'name']


@admin.register(UceSubjects)
class UceSubjectsAdmin(admin.ModelAdmin):
    list_display = ('name','category')
    ordering = ['category']
    search_fields = ['code', 'name']

