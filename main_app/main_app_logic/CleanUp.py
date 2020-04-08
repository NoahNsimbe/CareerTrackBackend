from datetime import datetime
from app_logic.AppExceptions import DatabaseError, AppError
from main_app.serializers import CourseSerializer, CutOffPointsSerializer
from main_app.models import Courses, CutOffPoints
import logging
logger = logging.getLogger(__name__)


def check_points(course, uace_results, uce_results, subjects, admission_type, gender):

    subsidiaries = subjects["desirable"]
    subsidiaries.append("UACE_GP")
    essentials = subjects["essential"]
    relevant = subjects["relevant"]
    principal_pass = ["A", "B", "C", "D", "E"]
    count = 0
    points = 0.0
    private_points = 0.0
    govt_points = 0.0

    grade_mappings = {"A": 6, "B": 5, "C": 4, "D": 3, "E": 2, "F": 1, "O": 0}

    try:
        year = datetime.now().year - 1

        cut_off = CutOffPointsSerializer(CutOffPoints.objects.filter(course=course, year=year), many=True).data

        if len(cut_off) > 2:
            raise DatabaseError("Course {} has more than two entries for cutoff points for the year {}"
                                .format(course, year))

        for i in cut_off:
            if str(i["type"]).upper() == "PRIVATE":
                private_points = i["points"]
            elif str(i["type"]).upper() == "PUBLIC":
                govt_points = i["points"]
            else:
                pass

        if private_points == 0.0 or govt_points == 0.0:
            # log warning
            pass

    except Exception as e:
        error = """
                An error occurred while processing cut off points for course '{}'
                Error Details : 
                {}""".format(course, e)

        raise AppError(error)

    for subject in subsidiaries:
        if subject in uace_results:
            if uace_results[subject] in range(1, 7):
                points = points + (uace_results[subject] * 1)
                del uace_results[subject]

    for subject in essentials:
        if subject in uace_results:
            if str(uace_results[subject]).upper() in principal_pass:
                count = count + 1
                points = points + (grade_mappings[uace_results[subject]] * 2) \
                    if count >= 3 else points + (grade_mappings[uace_results[subject]] * 3)
                del uace_results[subject]

    for subject in relevant:
        if subject in uace_results:
            if str(uace_results[subject]).upper() in principal_pass:
                points = points + (grade_mappings[uace_results[subject]] * 2)
                del uace_results[subject]

    for grade in uce_results.values():
        if grade in range(1, 3):
            points = points + 0.3
        elif grade in range(3, 7):
            points = points + 0.2
        elif grade in range(7, 9):
            points = points + 0.1
        else:
            pass

    if str(gender).upper() == "FEMALE":
        points = points + 1.5

    points = round(points, 1)

    if str(admission_type).upper() == "PRIVATE":
        return True if points >= private_points else False
    elif str(admission_type).upper() == "GOVERNMENT" or str(admission_type).upper() == "PUBLIC":
        return True if points >= govt_points else False
    else:
        return True


def format_output(recommended_codes, non_recommended_codes):

    recommended_courses_list = []
    non_recommended_courses_list = []

    for code in recommended_codes:
        course_details = CourseSerializer(Courses.objects.filter(code=code), many=True).data
        recommended_courses_list.append(course_details[0])

    for entry in non_recommended_codes:
        code = ""
        reason = ""
        for key in entry.keys():
            code = key
            break

        for value in entry.values():
            reason = value
            break

        course_details = CourseSerializer(Courses.objects.filter(code=code), many=True).data
        output = dict({"course": course_details[0], "Reason": reason})

        non_recommended_courses_list.append(output)

    return recommended_courses_list, non_recommended_courses_list
    pass
