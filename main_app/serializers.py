from rest_framework import serializers
from .models import Courses, CourseConstraints, CareerCourses, Careers, CourseSubjects, ALevelConstraints


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class CourseConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseConstraints
        fields = '__all__'


class CareerCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerCourses
        fields = '__all__'


class ALevelConstraintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALevelConstraints
        fields = '__all__'


class OLevelConstraintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALevelConstraints
        fields = '__all__'


class CourseSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubjects
        fields = ['subject']


class CareersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = '__all__'





class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = ['courses']
