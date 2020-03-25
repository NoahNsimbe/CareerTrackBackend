from main_app.serializers import CourseSerializer
from main_app.models import Courses


def compute_points(recommended_codes, non_recommended_codes, results, admission_type):
    #
    #

    recommended_courses_list = []
    non_recommended_courses_list = []

    for code in recommended_codes:
        course_details = CourseSerializer(Courses.objects.filter(code=code), many=True).data
        recommended_courses_list.append(course_details[0])

    for code in non_recommended_codes:
        course_details = CourseSerializer(Courses.objects.filter(code=code), many=True).data
        non_recommended_courses_list.append(course_details[0])

    return recommended_courses_list, non_recommended_courses_list
