from datetime import datetime
from app_logic.AppExceptions import DatabaseError, AppError
from main_app.serializers import CourseSerializer, CutOffPointsSerializer
from main_app.models import Courses, CutOffPoints


def check_points(course, uace_results, uce_results, uace_subjects, admission_type, gender):

    subsidiaries = uace_subjects["desirable"]
    essentials = uace_subjects["essential"]
    relevant = uace_subjects["relevant"]
    principal_pass = ["A", "B", "C", "D", "E"]
    count = 0
    points = 0.0
    private_points = 0.0
    govt_points = 0.0

    try:
        year = datetime.now().year - 1
        cut_off = CutOffPointsSerializer(CutOffPoints.objects.filter(course=course, year=year)).data

        if len(cut_off) > 2:
            raise DatabaseError("Course {} has more than two entries for cutoff points for the year {}"
                                .format(course, year))

        for i in cut_off:
            if str(i["type"]).upper() == "PRIVATE":
                private_points = i["points"]
            elif str(i["type"]).upper() == "GOVERNMENT":
                govt_points = i["points"]
            else:
                pass

        if private_points == 0.0 or govt_points == 0.0:
            # log warning
            pass

    except DatabaseError as e:
        error = """
                course '{}' has errors with its cut off points
                Error Details : 
                {}""".format(course, e)

        raise AppError(error)

    for subject in subsidiaries:
        if subject in uace_results:
            if uace_results[subject] in range(1, 7):
                points = points + (uace_results[subject] * 1)
                # remove it

    for subject in essentials:
        if subject in uace_results:
            if str(uace_results[subject]).upper() in principal_pass:
                count = count + 1
                points = points + (uace_results[subject] * 2) if count >= 3 else points + (uace_results[subject] * 3)

    for subject in relevant:
        if subject in uace_results:
            if str(uace_results[subject]).upper() in principal_pass:
                points = points + (uace_results[subject] * 2)

    for grade in uce_results.vales():
        if grade in range(1, 3):
            points = points + (grade * 0.3)
        elif grade in range(3, 7):
            points = points + (grade * 0.2)
        elif grade in range(7, 9):
            points = points + (grade * 0.1)
        else:
            pass

    if str(gender).upper() == "FEMALE":
        points = points + 1.5

    if str(admission_type).upper() == "PRIVATE":
        return True if points >= private_points else False
    elif str(admission_type).upper() == "GOVT" or str(admission_type).upper() == "GOVERNMENT":
        return True if points >= govt_points else False


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
