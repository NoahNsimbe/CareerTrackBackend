from rest_framework import status
from rest_framework.response import Response

from main_app.logic.AppExceptions import AppError
from main_app.logic.CleanUp import check_points, format_output
from main_app.logic.ConstraintCheck import check_constraints
from main_app.logic.SubjectCheck import check_subject
from main_app.models import CareerCourses, Courses
from main_app.serializers import CareerCoursesSerializer, CourseSerializer


def without_results(career):

    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data

    if career_courses:

        try:

            recommended_courses_list = []

            for career_course in career_courses:
                course_details = CourseSerializer(Courses.objects.filter(code=career_course["course"]), many=True).data
                recommended_courses_list.append(course_details[0])

            recommended_courses = dict()
            recommended_courses['programs'] = recommended_courses_list

        except Exception as exception:
            print("Exception Has occurred : \n {}".format(exception))
            errors = "Sorry, there was an error while processing information for the career '{}'".format(career)

            return False, None, errors

        return True, recommended_courses, None
        # return True, recommended_courses, None

    else:

        errors = "Sorry, we haven't yet updated our system to cater for '{}'".format(career)
        print(errors)

        return False, None, errors


def with_results(career, uace_results, uce_results, admission_type, gender):

    recommended_codes = []
    non_recommended_codes = []

    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data

    if career_courses:

        for career_course in career_courses:

            try:
                course_code = career_course["course"]

                # check whether user has all required course subjects
                check, subjects = check_subject(course_code, uace_results)

                if check:
                    # check whether user meets a and o level constraints on the course
                    if check_constraints(course_code, uace_results, uce_results, subjects):

                        if check_points(course_code, uace_results, uce_results, subjects, admission_type, gender):
                            recommended_codes.append(course_code)
                        else:
                            non_recommended_codes.append({course_code: "Your computed points are less the the "
                                                                       "cut off points for the previous year, "
                                                                       "we therefore don't recommend the course"})
                    else:
                        non_recommended_codes.append({course_code: "Some of your O or A level grades are below the "
                                                                   "minimum grades for the course"})
                else:
                    non_recommended_codes.append({course_code: "You are missing an essential, relevant "
                                                               "or desirable subject required for the course"})

            except AppError as exception:

                print("Exception Has occurred: \n {}".format(exception))

                errors = "Sorry, there was an error while processing information for the career '{}'".format(career)

                return False, None, errors

        recommended_courses, non_recommended_courses = format_output(recommended_codes, non_recommended_codes)

        recommendations = dict()
        recommendations["Recommended courses"] = recommended_courses
        recommendations["Non Recommended courses"] = non_recommended_courses

        return True, recommendations, None
        # return True, recommendations, None

    else:
        errors = "Sorry, we haven't yet updated our system to cater for {}".format(career)
        print(errors)
        return False, None, errors


def course_recommendation(data):
    career = data.get("career")
    admission_type = data.get("admission_type", None)
    uace_results = data.get("uace_results", None)
    uce_results = data.get("uce_results", None)
    gender = data.get("gender", None)

    if career is None or str(career) == "":
        return Response({'Message': "Please provide a career"}, status.HTTP_400_BAD_REQUEST)

    career = str(career).strip()

    if (admission_type is None or str(admission_type) == "") and (uace_results is None or uace_results == {}) and \
            (uce_results is None or uce_results == {}) and (gender is None or str(admission_type) == ""):

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