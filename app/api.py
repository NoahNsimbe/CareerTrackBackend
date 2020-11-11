from rest_framework import viewsets, filters, mixins, generics
from app.models import Careers, UaceSubjects, UceSubjects
from app.serializers import CareersSerializer, UaceCombinationSerializer, \
    CourseRecommendationSerializer, UaceSerializer, UceSerializer
from app.logic.Combination import uace_combination
from app.logic.Course import course_recommendation


class CombinationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UaceCombinationSerializer
    queryset = UceSubjects.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return uace_combination(serializer.data)


class ProgramViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CourseRecommendationSerializer
    queryset = UaceSubjects.objects.all()

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
    serializer_class = UaceSerializer
    queryset = UaceSubjects.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']


class UceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UceSerializer
    queryset = UceSubjects.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']
