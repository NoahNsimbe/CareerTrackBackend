from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .main_app_logic.Combination import get_combination
from .main_app_logic.Course import without_results, with_results
from .models import Careers, UceSubjects, UaceSubjects
from .serializers import CareersSerializer, UceSerializer, UaceSerializer
import json

@api_view(['GET'])
def careers(request):
    if request.method == 'GET':
        careers = Careers.objects.all()
        serializer = CareersSerializer(careers, many=True).data
        data = json.dumps(dict({"careers": [x["name"] for x in serializer]}))
        return Response(data)


@api_view(['GET'])
def uce_subjects(request):
    if request.method == 'GET':
        subjects = UceSubjects.objects.all()
        serializer = UceSerializer(subjects, many=True).data
        subjects = json.dumps(dict({"uce_subjects": [dict({x["code"]: x["name"]}) for x in serializer ] }))
        return Response(subjects)


@api_view(['GET'])
def uace_subjects(request):
    if request.method == 'GET':
        subjects = UaceSubjects.objects.all()
        serializer = UaceSerializer(subjects, many=True).data
        data = {"Science Subjects": [dict({x["code"]: x["name"]}) for x in serializer if x["category"] == "Science"],
                "Art Subjects": [dict({x["code"]: x["name"]}) for x in serializer if x["category"] == "Art"],
                "Subsidiary Subjects": [dict({x["code"]: x["name"]}) for x in serializer if x["category"] == "Subsidiary"]}
        subjects = json.dumps(dict({"uace_subjects": data}))
        return Response(subjects)


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
