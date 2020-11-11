from rest_framework import serializers
from .models import Courses, CourseConstraints, CareerCourses, Careers, CourseSubjects, ALevelConstraints, \
    OLevelConstraints, CutOffPoints, UaceSubjects, UceSubjects


class UaceCombinationSerializer(serializers.Serializer):
    career = serializers.CharField(required=True)
    uce_results = serializers.DictField(required=False)


class CourseRecommendationSerializer(serializers.Serializer):
    career = serializers.CharField(required=True)
    uce_results = serializers.DictField(required=False)
    admission_type = serializers.CharField(required=False)
    uace_results = serializers.DictField(required=False)
    gender = serializers.CharField(required=False)


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
