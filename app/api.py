from urllib import request

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, filters, mixins, generics, status
from rest_framework.decorators import api_view
from app.logic.Program import Program
from app.models import Careers, UaceSubjects, UceSubjects, Courses, Articles
from app.serializers import CareersSerializer, UaceCombinationSerializer, \
    CourseRecommendationSerializer, UaceSerializer, UceSerializer, CourseSerializer, ProgramSerializer, \
    ArticlesSerializer, UserSerializer
from app.logic.Combination import uace_combination, combination_recommendation
from app.logic.Course import course_recommendation, check_program_eligibility
from django.core.cache import cache


class ArticlesListViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                          mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['author', 'topic', 'featured']
    search_fields = ['author', 'author_image', 'title',
                     'article_image', 'read_time', 'bait', 'topic',
                     'body', 'claps', 'created_on', 'updated_on']

    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = str(x_forwarded_for.split(',')[0])
        else:
            ip = str(request.META.get('REMOTE_ADDR'))

        cached_data = cache.get(ip)

        if cached_data == str(instance.id):
            return Response({"message": "Already made a clap",
                             "article": instance.id,
                             "claps": instance.claps},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            cache.set(ip, str(instance.id), 86400)

        serializer = ArticlesSerializer(instance,
                                        data={"claps": instance.claps + 1},
                                        partial=True,
                                        context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"article": instance.id,
                         "claps": serializer.data["claps"]},
                        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return self.partial_update(request)


class ArticlesCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer


class UsersViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all().filter(is_staff=False, is_superuser=False)
    serializer_class = UserSerializer

    def get_permissions(self):

        if request == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


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


class ProgramDetailsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ProgramSerializer
    queryset = Courses.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'description']


class CareersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CareersSerializer
    queryset = Careers.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class UaceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UaceSerializer
    queryset = UaceSubjects.objects.all()
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'code']


class ProgramsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'description']


class UceViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UceSerializer
    queryset = UceSubjects.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']
    #
    # def create(self, request, *args, **kwargs):
    #
    #     program_details = Program(program_code='CSC').get_details()
    #
    #     print("\n\n")
    #     print(program_details)
    #
    #     return Response({"message": "okay"}, status=status.HTTP_200_OK)
    #
    #     data = request.data
    #
    #     if 'requestType' not in data:
    #         return Response(
    #             {
    #                 "message": "missing requestType : " + AppRequests.value
    #              }
    #             , status=status.HTTP_400_BAD_REQUEST)
    #
    #     if data['requestType'] == AppRequests.UceProgram:
    #         if 'program' not in data:
    #             return Response({"message": "missing data"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #         program = data['program']
    #
    #     elif data['requestType'] == AppRequests.UceProgramResults:
    #         if 'program' not in data or 'uce_results' not in data:
    #             return Response({"message": "missing data"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #         program = data['program']
    #         uce_results = data['uce_results']
    #
    #     else:
    #         return Response({"message": "missing data"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return course_recommendation(serializer.data)


@api_view(['POST'])
def program_details(request):
    try:
        program_code = request.data["program_code"]
    except KeyError:
        return Response({"message": "provide a program_code"}, status=status.HTTP_400_BAD_REQUEST)

    details = Program(program_code=program_code).get_details()

    return Response({"details": details}, status=status.HTTP_200_OK)


@api_view(['POST'])
def program_eligibility(request):
    try:
        program_code = request.data["program_code"]
        uce_results = request.data["uce_results"]
        uace_results = request.data["uace_results"]
        gender = request.data["gender"]
        admission_type = request.data["admission_type"]
    except KeyError:
        return Response({"message": "provide all required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = check_program_eligibility(program_code=program_code,
                                             uace_results=uace_results,
                                             uce_results=uce_results,
                                             gender=gender, admission_type=admission_type)
        return Response({"check": response}, status=status.HTTP_200_OK)

    except Exception:
        return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def recommend_combination(request):
    try:
        program_code = request.data["program_code"]
    except KeyError:
        return Response({"message": "provide all required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = combination_recommendation(program_code=program_code)
        return Response(response, status=status.HTTP_200_OK)

    except Exception:
        return Response({"message": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
