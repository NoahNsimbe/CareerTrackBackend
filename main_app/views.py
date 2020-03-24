from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from subjects.models import UaceSubjects
from subjects.serializers import UaceOptionalsSerializer
from .models import Courses, CareerCourses, Careers, CourseConstraints, CourseSubjects
from .serializers import CourseSubjectsSerializer, CourseSerializer, CareerCoursesSerializer, CareersSerializer, \
    CoursesSerializer, CourseConstraintsSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView


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


@api_view(['GET'])
def get_careers(request):
    if request.method == 'GET':
        careers = Careers.objects.all()
        serializer = CareersSerializer(careers, many=True).data
        data = {"careersList": [x["name"] for x in serializer]}
        return Response(data)


class CareersClass(APIView):
    def get(self, request):
        careers = Careers.objects.all()
        serializer = CareersSerializer(careers, many=True).data
        data = {"careersList": [x["name"] for x in serializer]}
        return Response(data)


@api_view(['POST'])
def signup(request):

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    last_name = request.data.get('last_name')
    first_name = request.data.get('first_name')

    if all(parameter is None for parameter in [username, email, password, last_name, first_name]):

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


@api_view(['POST'])
def course_without_results(request):

    career = request.data.get("career")

    if career is None:
        return Response({'Message': "Please provide a career"}, status.HTTP_400_BAD_REQUEST)

    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data

    if career_courses:

        recommended_courses = {}
        recommended_courses_list = []

        for career_course in career_courses:

            course_details = CourseSerializer(Courses.objects.filter(code=career_course["course"]), many=True).data
            recommended_courses_list.append(course_details[0])

        recommended_courses['programs'] = recommended_courses_list

        return Response(recommended_courses, status.HTTP_200_OK)

    else:
        return Response({'Message': 'Currently, the system cannot get recommended courses for this career'},
                        status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def course_with_results(request):

    career = request.data.get("career")
    admission_type = request.data.get("admission_type")
    uace_results = request.data.get("uace_results")

    if (career is None) or (admission_type is None) or (uace_results is None):
        return Response({'Message': "Please provide all fields"}, status.HTTP_400_BAD_REQUEST)

    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data

    if career_courses:
        for career_course in career_courses:
            course_code = career_course["course"]

            constraints = CourseConstraintsSerializer(CourseConstraints.objects.filter(course=course_code))
            no_of_essentials = constraints['essentials']
            no_of_relevant = constraints['relevant']
            desirable_state = constraints['desirable_state']
            desirable_check = False
            relevant_check = False

            try:
                essential_check, essential_subjects = check_essentials(course_code, no_of_essentials, uace_results)

                if essential_check:
                    relevant_check, relevant_subjects = check_relevant(course_code, no_of_essentials, uace_results)

                if relevant_check:
                    desirable_check, desirable_subjects = check_desirable(course_code, desirable_state, uace_results)

            except Exception as ex:

                # log error args informing admins of database incorrect entries
                return Response({'Message': 'There was an error on database'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

            if desirable_check:
                pass

    else:
        return Response({'Message': 'Currently, the system cannot get recommended courses for this career'},
                        status.HTTP_204_NO_CONTENT)


def check_desirable(course, state, results):
    if state == 1:
        try:
            subject = CourseSubjectsSerializer(CourseSubjects.objects.filter(category="desirable", course=course)).data

        except AttributeError:
            return Response(
                {'Message': "Essential subject expected to be one but found many"},
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return True if subject in results else False, subject

    elif state == 2:
        subjects = UaceOptionalsSerializer(UaceSubjects.objects.filter(category="optional")).data
        return True, subjects
    pass


def check_relevant(course, number, results):

    if number == 1:

        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="relevant", course=course), many=True).data

        count = 0
        for subject in results:
            if subject in subjects:
                count = count+1

        if count == 2:
            return True, subjects
        elif count < 2:
            return False, subjects
        else:
            # raise an error
            pass

    elif number == 2:
        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="relevant", course=course), many=True
        ).data

        count = 0
        for subject in results:
            if subject in subjects:
                count = count + 1

        if count == 1:
            return True, subjects
        elif count < 1:
            return False, subjects
        else:
            # raise an error
            pass

    elif number == 3:
        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="relevant", course=course), many=True
        ).data

        for subject in results:
            if subject in subjects:
                return True, subjects

        return False, subjects

    else:
        # raise error in case number of essentials is greater than 3
        pass


def check_essentials(course, number, results):

    if number == 1:

        try:
            subject = CourseSubjectsSerializer(CourseSubjects.objects.filter(category="essential", course=course)).data

        # raise error incase more the once essential is found in database

        except AttributeError:
            return Response(
                {'Message': "Essential subject expected to be one but found many"},
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return True if subject in results else False, subject

    elif number == 2:
        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="essential", course=course), many=True
        ).data

        for subject in subjects:
            if subject not in results:
                return False, subjects

        return True, subjects

    elif number == 3:
        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="essential", course=course), many=True
        ).data

        for subject in subjects:
            if subject in results:
                return True, subjects

        return False, subjects

    else:
        # raise error in case number of essentials is greater than 3
        pass