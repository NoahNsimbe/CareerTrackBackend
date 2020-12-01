from rest_framework.response import Response
from rest_framework import viewsets, filters, mixins, generics, status
from rest_framework.decorators import api_view
from app.logic.Program import Program
from app.models import Careers, UaceSubjects, UceSubjects, AppRequests, Courses
from app.serializers import CareersSerializer, UaceCombinationSerializer, \
    CourseRecommendationSerializer, UaceSerializer, UceSerializer, CourseSerializer
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
    filterset_fields = ['category']
    search_fields = ['name', 'code']


@api_view(['POST'])
def program_details(request):
    try:
        program_code = request.data["program_code"]
    except KeyError:
        return Response({"message": "provide a program_code"}, status=status.HTTP_400_BAD_REQUEST)

    details = Program(program_code=program_code).get_details()

    return Response({"details": details}, status=status.HTTP_200_OK)


class ProgramsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'description']


class UceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UceSerializer
    queryset = UceSubjects.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']

    def create(self, request, *args, **kwargs):

        program_details = Program(program_code='CSC').get_details()

        print("\n\n")
        print(program_details)

        return Response({"message": "okay"}, status=status.HTTP_200_OK)

        data = request.data

        if 'requestType' not in data:
            return Response(
                {
                    "message": "missing requestType : " + AppRequests.value
                 }
                , status=status.HTTP_400_BAD_REQUEST)

        if data['requestType'] == AppRequests.UceProgram:
            if 'program' not in data:
                return Response({"message": "missing data"}, status=status.HTTP_400_BAD_REQUEST)

            program = data['program']

        elif data['requestType'] == AppRequests.UceProgramResults:
            if 'program' not in data or 'uce_results' not in data:
                return Response({"message": "missing data"}, status=status.HTTP_400_BAD_REQUEST)

            program = data['program']
            uce_results = data['uce_results']

        else:
            return Response({"message": "missing data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return course_recommendation(serializer.data)
