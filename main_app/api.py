from rest_framework import viewsets, filters, mixins
from main_app.models import Careers, UaceSubjects, UceSubjects
from main_app.serializers import CareersSerializer, UaceViewSerializer, UceViewSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main_app.logic.Combination import get_combination
from main_app.logic.Course import without_results, with_results


@api_view(['POST'])
def uace_combination(request):

    career = request.data.get("career")
    uce_results = request.data.get("uce_results")

    if career is None or str(career) == "":
        return Response({'Message': "Please provide a career"}, status.HTTP_400_BAD_REQUEST)

    elif uce_results is None:
        success, results, errors = get_combination(career, [])

    else:
        career = str(career).strip()
        success, results, errors = get_combination(career, uce_results)

    if success:
        return Response(results, status.HTTP_200_OK)

    else:
        response = {'Message': errors}
        return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def course_recommendation(request):
    career = request.data.get("career")
    admission_type = request.data.get("admission_type")
    uace_results = request.data.get("uace_results")
    uce_results = request.data.get("uce_results")
    gender = request.data.get("gender")

    if career is None or str(career) == "":
        return Response({'Message': "Please provide a career"}, status.HTTP_400_BAD_REQUEST)

    career = str(career).strip()

    if (admission_type is None) and (uace_results is None) and (uce_results is None) and (gender is None):
        success, results, errors = without_results(career)

    elif admission_type is None:
        return Response({
            'Message': "Please provide an admission type, private and public admission are the available options"
        }, status.HTTP_400_BAD_REQUEST)

    elif gender is None:
        return Response({'Message': "Please specify your gender"}, status.HTTP_400_BAD_REQUEST)

    elif uace_results is None:
        return Response({'Message': "Please provide your uace results"}, status.HTTP_400_BAD_REQUEST)

    elif uce_results is None:
        return Response({'Message': "Please provide your uce results"}, status.HTTP_400_BAD_REQUEST)

    else:
        success, results, errors = with_results(career, uace_results, uce_results, admission_type, gender)

    if success:
        return Response(results, status.HTTP_200_OK)

    else:
        response = {'Message': errors}
        return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


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
