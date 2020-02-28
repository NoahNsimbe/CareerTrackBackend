from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from .models import Careers
from .serializers import CareersSerializer


@api_view(['GET'])
def get_careers(request):
    if request.method == 'GET':
        careers = Careers.objects.all()
        serializer = CareersSerializer(careers, many=True).data
        data = {"careersList": [x["name"] for x in serializer]}
        return JsonResponse(data, safe=False)
