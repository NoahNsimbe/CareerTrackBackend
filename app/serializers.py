from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Courses, CourseConstraints, CareerCourses, Careers, CourseSubjects, ALevelConstraints, \
    OLevelConstraints, CutOffPoints, UaceSubjects, UceSubjects, Articles


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
        # fields = '__all__'
        exclude = ['id']


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
        exclude = ['id']


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
        model = Courses
        fields = ['courses']


class UaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UaceSubjects
        fields = '__all__'


class UceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UceSubjects
        fields = '__all__'


class CutOfPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CutOffPoints
        fields = '__all__'


class ALevelConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ALevelConstraints
        fields = '__all__'


class OLevelConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OLevelConstraints
        fields = '__all__'


class ProgramDetailsSerializer(serializers.Serializer):
    program = CourseSerializer(required=True)
    cut_off_points = CutOffPointsSerializer(required=False)
    program_constraints = CourseConstraintsSerializer(required=False)
    program_subjects = CourseSubjectsSerializer(required=False)
    a_level_constraints = ALevelConstraintSerializer(required=False)
    o_level_constraints = OLevelConstraintSerializer(required=False)


class UceRecommendationSerializer(serializers.ModelSerializer):
    program = CoursesSerializer(required=False)
    uce_results = serializers.DictField(required=False)


class ArticlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Articles
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'last_name', 'username']
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    cutOfPoints = CutOfPointsSerializer(required=False)
    OLevelConstraints = OLevelConstraintsSerializer(required=False)
    ALevelConstraints = ALevelConstraintsSerializer(required=False)

    class Meta:
        model = Courses
        fields = '__all__'


