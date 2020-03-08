from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from careers.models import Careers
from careers.serializers import CareersSerializer, CoursesSerializer

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


@api_view('POST')
def combination_without_results(request):

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
