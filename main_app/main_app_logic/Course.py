from rest_framework.utils import json
from app_logic.AppExceptions import AppError
from .ComputePoints import compute_points
from .ConstraintCheck import check_course_constraints
from .SubjectCheck import check_course_subjects
from main_app.models import CareerCourses, Courses
from main_app.serializers import CareerCoursesSerializer, CourseSerializer


def without_results(career):

    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data

    if career_courses:

        recommended_courses_list = []

        for career_course in career_courses:
            course_details = CourseSerializer(Courses.objects.filter(code=career_course["course"]), many=True).data
            recommended_courses_list.append(course_details[0])

        recommended_courses = dict()
        recommended_courses['programs'] = recommended_courses_list

        return True, json.dumps(recommended_courses), None

    else:
        # log error args informing admins of database incorrect entries

        errors = "Sorry, we haven't yet updated our system to cater for '{}'".format(career)
        return False, None, errors


def with_results(career, uace_results, admission_type):

    recommended_codes = []
    non_recommended_codes = []

    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data

    if career_courses:

        for career_course in career_courses:
            course_code = career_course["course"]

            # check whether user has all required course subjects
            try:
                course_subjects_present = check_course_subjects(course_code, uace_results)

                if not course_subjects_present:
                    non_recommended_codes.append(course_code)

            except AppError as exception:
                # log error args informing admins of database incorrect entries

                errors = "Sorry, there was an error while processing information for the career '{}'"\
                    .format(career)

                return False, None, errors

            # check whether user meets a and o level constraints on the course
            if course_subjects_present:

                try:
                    secondary_constraint_check = check_course_constraints(course_code, uace_results)

                    if secondary_constraint_check:
                        recommended_codes.append(course_code)
                    else:
                        non_recommended_codes.append(course_code)

                except AppError as exception:
                    # log error args informing admins of database incorrect entries
                    errors = "Sorry, there was an error while processing information for the career '{}'" \
                        .format(career)

                    return False, None, errors

        recommended_courses, non_recommended_courses = compute_points(recommended_codes, non_recommended_codes,
                                                                      uace_results, admission_type)

        courses = dict()
        courses["Recommended courses"] = recommended_courses
        courses["Non Recommended courses"] = non_recommended_courses

        return True, json.dumps(courses), None

    else:

        errors = "Sorry, we haven't yet updated our system to cater for {}".format(career)
        return False, None, errors
