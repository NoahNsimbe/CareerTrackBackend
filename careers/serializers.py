from rest_framework import serializers
from .models import Careers


class CareersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = '__all__'
