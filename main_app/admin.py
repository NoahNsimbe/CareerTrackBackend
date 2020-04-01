from django.contrib import admin
from .models import Careers, Courses, CareerCourses, CourseConstraints, ALevelConstraints, CourseSubjects, \
    OLevelConstraints


@admin.register(Careers)
class CareersAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ['name']
    search_fields = ('name', 'description')


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


@admin.register(CourseConstraints)
class CourseConstraintsAdmin(admin.ModelAdmin):
    list_display = ('course', 'essentials', 'relevant','desirable_state', 'subject_constraint', 'a_level_constraint',
                    'o_level_constraint', 'all_subjects')
    ordering = ['course']
    search_fields = ['course__code', 'course__name']


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
    # list_filter = ('course__name')


@admin.register(OLevelConstraints)
class OLevelConstraintsAdmin(admin.ModelAdmin):
    list_display = ('code', 'subject', 'maximum_grade')
    ordering = ['code']
    search_fields = ['code__code', 'code__name', 'subject__code']

    # def active(self, obj):
    #     return obj.is_active == 1
    #
    # active.boolean = True


# models = [Courses, CareerCourses, CourseConstraints, CourseSubjects, ALevelConstraints, OLevelConstraints]
# admin.site.register(models)
