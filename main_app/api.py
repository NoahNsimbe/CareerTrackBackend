from rest_framework import viewsets, filters, mixins
from main_app.models import Careers, UaceSubjects, UceSubjects
from main_app.serializers import CareersSerializer, UaceViewSerializer, UceViewSerializer, UaceCombinationSerializer, \
    CourseRecommendationSerializer
from main_app.logic.Combination import uace_combination
from main_app.logic.Course import course_recommendation


class UaceCombinationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UaceCombinationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return uace_combination(serializer.data)


class CourseRecommendationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CourseRecommendationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return course_recommendation(serializer.data)


class CareersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CareersSerializer
    queryset = Careers.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class UaceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UaceViewSerializer
    queryset = UaceSubjects.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']


class UceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UceViewSerializer
    queryset = UceSubjects.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']
