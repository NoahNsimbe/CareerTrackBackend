from rest_framework import serializers
from .models import Courses, CourseConstraints


class CourseSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['essential', 'relevant', 'desirable', 'description', 'name']


class CourseConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseConstraints
        fields = ['no_of_essential', 'no_of_relevant']