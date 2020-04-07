from app_logic.AppExceptions import AppError
from .CleanUp import check_points, format_output
from .ConstraintCheck import check_constraints
from .SubjectCheck import check_subject
from main_app.models import CareerCourses, Courses
from main_app.serializers import CareerCoursesSerializer, CourseSerializer

import logging
logger = logging.getLogger(__name__)


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
            logger.error("Exception Has occurred : \n {}".format(exception))
            errors = "Sorry, there was an error while processing information for the career '{}'".format(career)

            return False, None, errors

        # return True, json.dumps(recommended_courses), None
        return True, recommended_courses, None

    else:

        errors = "Sorry, we haven't yet updated our system to cater for '{}'".format(career)
        logger.error(errors)

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

                logger.error("Exception Has occurred: \n {}".format(exception))

                errors = "Sorry, there was an error while processing information for the career '{}'".format(career)

                return False, None, errors

        # compute cut-off points, sort and return recommendations
        # recommended_courses, non_recommended_courses = check_points(recommended_codes, non_recommended_codes,
        #                                                             uace_results, admission_type)

        recommended_courses, non_recommended_courses = format_output(recommended_codes, non_recommended_codes)

        recommendations = dict()
        recommendations["Recommended courses"] = recommended_courses
        recommendations["Non Recommended courses"] = non_recommended_courses

        # return True, json.dumps(recommendations), None
        return True, recommendations, None

    else:
        errors = "Sorry, we haven't yet updated our system to cater for {}".format(career)
        logger.error(errors)
        return False, None, errors
