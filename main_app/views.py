from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .main_app_logic.Combination import get_combination
from .main_app_logic.Course import without_results, with_results
from .models import Careers
from .serializers import CareersSerializer


@api_view(['GET'])
def get_careers(request):
    if request.method == 'GET':
        careers = Careers.objects.all()
        serializer = CareersSerializer(careers, many=True).data
        data = {"careersList": [x["name"] for x in serializer]}
        return Response(data)


@api_view(['POST'])
def uace_combination(request):

    career = request.data.get("career")
    uce_results = request.data.get("uce_results")

    if career is None:
        return Response({'Message': "Please provide a career"}, status.HTTP_400_BAD_REQUEST)

    elif uce_results is None:
        success, results, errors = get_combination(career, [])

    else:
        success, results, errors = get_combination(career, uce_results)

    if success:
        return Response(results, status.HTTP_200_OK)

    else:
        response = {'Message': errors}
        return Response(response, status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def course_recommendation(request):
    career = request.data.get("career")
    admission_type = request.data.get("admission_type")
    uace_results = request.data.get("uace_results")
    uce_results = request.data.get("uce_results")

    if career is None:
        return Response({'Message': "Please provide a career"}, status.HTTP_400_BAD_REQUEST)

    if (admission_type is None) and (uace_results is None) and (uce_results is None):
        success, results, errors = without_results(career)

    elif admission_type is None:
        return Response({
            'Message': "Please provide an admission type, private or public admission are the available options"
        }, status.HTTP_400_BAD_REQUEST)

    elif uace_results is None:
        return Response({'Message': "Please provide your uace results"}, status.HTTP_400_BAD_REQUEST)

    elif uce_results is None:
        return Response({'Message': "Please provide your uce results"}, status.HTTP_400_BAD_REQUEST)

    else:
        success, results, errors = with_results(career, uace_results, uce_results, admission_type)

    if success:
        return Response(results, status.HTTP_200_OK)

    else:
        response = {'Message': errors}
        return Response(response, status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def post_collection(request):
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         data = {'text': request.DATA.get('the_post'), 'author': request.user.pk}
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CareersClass(APIView):
#     def get(self, request):
#         careers = Careers.objects.all()
#         serializer = CareersSerializer(careers, many=True).data
#         data = {"careersList": [x["name"] for x in serializer]}
#         return Response(data)
#
#
# @api_view(['POST'])
# def signup(request):
#
#     username = request.data.get('username')
#     email = request.data.get('email')
#     password = request.data.get('password')
#     last_name = request.data.get('last_name')
#     first_name = request.data.get('first_name')
#
#     if all(parameter is None for parameter in [username, email, password, last_name, first_name]):
#
#         message = {'Message': "Please provide all necessary fields"}
#         return Response(message, status.HTTP_400_BAD_REQUEST)
#
#     if User.objects.filter(username=username).exists():
#         return Response(None, status.HTTP_409_CONFLICT)
#
#     try:
#         user = User.objects.create_user(username, email, password)
#         user.last_name = last_name
#         first_name = user.first_name = first_name
#         user.save()
#
#         message_body = 'Dear ' + first_name + ', Your account has successfully been created'
#         message = {'Message': message_body}
#
#         return Response(message, status.HTTP_201_CREATED)
#
#     except Exception:
#
#         message_body = "An error occurred while registering you"
#         message = {'Message': message_body}
#
#         return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def testing(request):
#
#     message = {'Message': 'Successful'}
#
#     return Response(message, status.HTTP_200_OK)
