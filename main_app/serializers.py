from abc import ABC

from rest_framework import serializers
from .models import Courses, CourseConstraints, CareerCourses, Careers, CourseSubjects, ALevelConstraints, \
    OLevelConstraints, CutOffPoints, UaceSubjects, UceSubjects


class UaceCombinationSerializer(serializers.Serializer):

    career = serializers.CharField()
    uce_results = serializers.DictField()


class CourseRecommendationSerializer(serializers.Serializer):
    career = serializers.CharField()
    uce_results = serializers.DictField()
    admission_type = serializers.CharField()
    uace_results = serializers.DictField()
    gender = serializers.CharField()


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
        model = OLevelConstraints
        fields = '__all__'


class CourseSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubjects
        fields = '__all__'


class CutOffPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CutOffPoints
        fields = '__all__'


class CareersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = '__all__'


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = ['courses']


class UaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UaceSubjects
        fields = '__all__'


class UceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UceSubjects
        fields = '__all__'


class UaceViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UaceSubjects
        fields = ('code', 'name', )


class UceViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UceSubjects
        fields = ('code', 'name', )
