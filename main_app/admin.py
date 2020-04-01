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
    # ordering = ['career']
    # search_fields = ('career', 'course')


@admin.register(CourseConstraints)
class CourseConstraintsAdmin(admin.ModelAdmin):
    list_display = ('course', 'essentials', 'relevant','desirable_state', 'subject_constraint', 'a_level_constraint',
                    'o_level_constraint', 'all_subjects')
    # ordering = ['course']
    # search_fields = ['course']


@admin.register(ALevelConstraints)
class ALevelConstraintsAdmin(admin.ModelAdmin):
    list_display = ('code', 'subject', 'minimum_grade')
    ordering = ['code']
    # search_fields = ['code']


@admin.register(CourseSubjects)
class CourseSubjectsAdmin(admin.ModelAdmin):
    list_display = ('course', 'subject', 'category', 'compulsory_state')
    ordering = ['course']
    # search_fields = ['course']


@admin.register(OLevelConstraints)
class OLevelConstraintsAdmin(admin.ModelAdmin):
    list_display = ('code', 'subject', 'maximum_grade')
    ordering = ['code']
    # search_fields = ['code']

    # def active(self, obj):
    #     return obj.is_active == 1
    #
    # active.boolean = True


# models = [Courses, CareerCourses, CourseConstraints, CourseSubjects, ALevelConstraints, OLevelConstraints]
# admin.site.register(models)
