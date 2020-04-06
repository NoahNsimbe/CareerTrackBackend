from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import UaceSubjects
from .serializers import UaceSerializer
from .models import UceSubjects
from .serializers import UceSerializer
from rest_framework.response import Response


@api_view(['GET'])
def get_uce(request):
    if request.method == 'GET':
        subjects = UceSubjects.objects.all()
        # subjects = get_object_or_404(UceSubjects)
        serializer = UceSerializer(subjects, many=True).data
        data = {"subjects": [x["name"] for x in serializer]}
        # return Response(serializer.data)
        return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_uace(request):
    if request.method == 'GET':
        subjects = UaceSubjects.objects.all()
        serializer = UaceSerializer(subjects, many=True).data
        data = {"compulsory": [x["name"] for x in serializer if x["category"] == "compulsory"],
                "subsidiaries": [x["name"] for x in serializer if x["category"] == "subsidiaries"],
                "optionals": [x["name"] for x in serializer if x["category"] == "optionals"]}
        return JsonResponse(data, safe=False)

