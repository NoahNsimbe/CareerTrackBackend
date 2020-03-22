from rest_framework import serializers
from .models import Courses, CourseConstraints, CareerCourses, Careers


class CourseSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['essential', 'relevant', 'desirable', 'description', 'name']


class CourseConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseConstraints
        fields = ['no_of_essential', 'no_of_relevant']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class CareerCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerCourses
        fields = '__all__'


class CareersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = '__all__'


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = ['courses']
