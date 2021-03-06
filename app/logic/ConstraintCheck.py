from app.logic.AppExceptions import AppError
from app.serializers import ALevelConstraintSerializer,  OLevelConstraintSerializer
from app.models import ALevelConstraints, OLevelConstraints


def check_a_level(course, a_level_results, o_level_results, principals):

    principal_pass = ["A", "B", "C", "D", "E"]
    count = 0

    for subject in principals:
        if subject in a_level_results:
            if a_level_results[subject] in principal_pass:
                count = count + 1

    if count < 2:
        return False

    course_constraints = ALevelConstraintSerializer(ALevelConstraints.objects.filter(code=course), many=True).data

    if course_constraints:

        try:

            for constraint in course_constraints:

                if a_level_results[constraint['subject']] < constraint['minimum_grade']:
                    if not check_o_level(course, o_level_results, True):
                        return False

        except Exception as details:
            error = """Error while checking A level subject constraints for course '{}'.
             Error Details : '{}'""".format(course, details)
            raise AppError(error)

    return True


def check_o_level(course, results, from_a_level=False):

    pass_grade = 8
    count = 0
    print(results)
    for grade in results.values():
        print(grade)
        if int(grade) <= pass_grade:
            count = count + 1

    if count < 5:
        return False

    course_constraints = OLevelConstraintSerializer(OLevelConstraints.objects.filter(code=course), many=True).data

    if course_constraints:

        try:

            for constraint in course_constraints:

                if constraint["subject"] in results:

                    if constraint["mandatory"] or from_a_level:

                        if results[constraint['subject']] > constraint['maximum_grade']:
                            return False

                elif constraint["mandatory"] or from_a_level:
                    return False

                else:
                    pass

        except Exception as details:

            error = """Error while checking O level subject constraints for course '{}'.
             Error Details : '{}'""".format(course, details)

            raise AppError(error)

    return True


def check_constraints(course_code, uace_results, uce_results, subjects):
    principals = subjects["essential"] + subjects["relevant"]

    if check_a_level(course_code, uace_results, uce_results, principals):

        if check_o_level(course_code, uce_results):

            return True

    return False
