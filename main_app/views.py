from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from careers.models import Careers
from careers.serializers import CareersSerializer, CoursesSerializer
from django.contrib.auth.models import User

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
from .models import Courses, CourseConstraints
from .serializers import CourseSubjectsSerializer, CourseConstraintsSerializer

from django.contrib.auth.models import User


@api_view(['POST'])
def signup(request):

    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        last_name = request.data.get('last_name')
        first_name = request.data.get('first_name')

    except Exception:

        message = {'Message': "Please provide all necessary fields"}
        return Response(message, status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response(None, status.HTTP_409_CONFLICT)

    try:
        user = User.objects.create_user(username, email, password)
        user.last_name = last_name
        first_name = user.first_name = first_name
        user.save()

        message_body = 'Dear ' + first_name + ', Your account has successfully been created'
        message = {'Message': message_body}

        return Response(message, status.HTTP_201_CREATED)

    except Exception:

        message_body = "An error occurred while registering you"
        message = {'Message': message_body}

        return Response(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def testing(request):

    message = {'Message': 'Successful'}

    return Response(message, status.HTTP_200_OK)


@api_view(['POST'])
def combination_without_results(request):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    if request.method == 'POST':
        # data = {'career': request.DATA.get('career')}
        # data = get_object_or_404(Careers, name=request.DATA.get('career'))
        career = get_object_or_404(Careers, name='doctor')
        # try:
        #     post = Post.objects.get(pk=pk)
        # except Post.DoesNotExist:
        #     return HttpResponse(status=404)

        career_courses = CoursesSerializer(career).data
        career_courses_codes = career_courses['courses'].split('/')

        recommendations = {}

        for course_code in career_courses_codes:

            course = ""

            try:

                course = get_object_or_404(Courses, code=course_code)
                course_details = CourseSubjectsSerializer(course).data

                course_name = course_details['name']
                course_description = course_details['description']
                essential = course_details['essential']
                relevant = course_details['relevant']
                desirable = course_details['desirable']

                recommendations[course_name] = {}
                recommendations[course_name]['description'] = course_description
                recommendations[course_name]['essential'] = essential
                recommendations[course_name]['relevant'] = relevant
                recommendations[course_name]['desirable'] = desirable
                recommendations[course_name]['desirable'] = desirable
                recommendations[course_name]['GP'] = 'General Paper'


                # try:
                #     course_constraints = get_object_or_404(CourseConstraints, code=course_code)
                #     constraint_details = CourseConstraintsSerializer(course_constraints).data
                #
                #     no_of_essential = constraint_details['no_of_essential']
                #     no_of_relevant = constraint_details['no_of_relevant']
                #
                #     essential = course_details['essential']
                #     relevant = course_details['relevant']
                #     desirable = course_details['desirable']
                #
                #     if no_of_essential == essential:
                #         recommendations[course_name]['essential'] = essential
                #
                #     elif no_of_essential < essential:
                #
                # except course_constraints.DoesNotExist:
                #     pass

            except course.DoesNotExist:
                pass

        return Response(recommendations, status=status.HTTP_200_OK)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
