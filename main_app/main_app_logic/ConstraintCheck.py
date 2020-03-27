from app_logic.AppExceptions import AppError
from main_app.serializers import ALevelConstraintSerializer,  OLevelConstraintSerializer
from main_app.models import ALevelConstraints, OLevelConstraints


def check_a_level(course, a_level_results, o_level_results):

    course_constraints = ALevelConstraintSerializer(ALevelConstraints.objects.filter(code=course), many=True).data

    if course_constraints:

        try:

            for constraint in course_constraints:

                if a_level_results[constraint['subject']] < constraint['minimum_grade'] and constraint['mandatory']:
                    return False

                if a_level_results[constraint['subject']] < constraint['minimum_grade'] and not constraint['mandatory']:
                    if not check_o_level(course, o_level_results):
                        return False

        except (AttributeError, KeyError) as details:
            error = """Error while checking A level subject constraints for course '{}'.
             Error Details : '{}'""".format(course, details)
            raise AppError(error)

    else:
        return True


def check_o_level(course, results):

    course_constraints = OLevelConstraintSerializer(OLevelConstraints.objects.filter(code=course), many=True).data

    if course_constraints:

        try:

            for constraint in course_constraints:

                if results[constraint['subject']] > constraint['maximum_grade'] and constraint['mandatory']:
                    return False

        except (AttributeError, KeyError) as details:

            error = """Error while checking O level subject constraints for course '{}'.
             Error Details : '{}'""".format(course, details)

            raise AppError(error)
    else:
        return True


def check_course_constraints(course_code, uace_results, uce_results):

    if check_a_level(course_code, uace_results, uce_results):

        if check_o_level(course_code, uce_results):

            return True

    return True
