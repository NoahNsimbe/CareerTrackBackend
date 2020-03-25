from .SubjectCheck import check_essentials, check_desirable, check_relevant
from main_app.models import CareerCourses, Courses, CourseConstraints
from main_app.serializers import CareerCoursesSerializer, CourseSerializer, CourseConstraintsSerializer


def without_results(career):
    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data
    errors = None
    recommended_courses = {}

    if career_courses:

        recommended_courses_list = []

        for career_course in career_courses:
            course_details = CourseSerializer(Courses.objects.filter(code=career_course["course"]), many=True).data
            recommended_courses_list.append(course_details[0])

        recommended_courses['programs'] = recommended_courses_list

        return True, recommended_courses, errors

    else:

        errors = "system does not have courses for career : " + career

        return False, recommended_courses, errors


def with_results(career, uace_results, admission_type):

    recommended_courses = []
    non_recommended_courses = []
    system_errors = None
    courses = {}

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
            essential_check = False
            course_subjects_present = False

            try:
                essential_check, essential_subjects = check_essentials(course_code, no_of_essentials, uace_results)

                if essential_check:
                    relevant_check, relevant_subjects = check_relevant(course_code, no_of_essentials, uace_results)

                if relevant_check:
                    desirable_check, desirable_subjects = check_desirable(course_code, desirable_state, uace_results)

                course_subjects_present = True if desirable_check else False

            except Exception:

                # log error args informing admins of database incorrect entries
                # return Response({'Message': 'There was an error on database'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

                system_errors = Exception
                return False, courses, system_errors

            if course_subjects_present:
                recommended_courses.append(course_code)

    else:
        system_errors = "system does not have courses for career : " + career
        return False, courses, system_errors

    # if recommended_courses:
    #     pass
