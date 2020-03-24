from rest_framework import serializers
from .models import UaceSubjects, UceSubjects


class UaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UaceSubjects
        fields = '__all__'


class UaceOptionalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UaceSubjects
        fields = ['name']


class UceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UceSubjects
        fields = '__all__'



