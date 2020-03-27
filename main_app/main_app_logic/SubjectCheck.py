from app_logic.AppExceptions import AppError, DatabaseError
from main_app.models import CourseSubjects, CourseConstraints
from main_app.serializers import CourseSubjectsSerializer, CourseConstraintsSerializer

import logging
logger = logging.getLogger(__name__)


def check_desirable(course, state, results):

    db_subjects = CourseSubjectsSerializer(
        CourseSubjects.objects.filter(category="desirable", course=course), many=True
    ).data

    if not db_subjects:
        error = """course '{}' has errors with its desirable subjects
                   Error Details : 
                   Doesnt have desirable subjects""".format(course)
        raise AppError(error)

    try:
        subjects = [x['subject'] for x in db_subjects]
    except KeyError as exception:
        error = """There was an error while checking subjects
                   Error Details
                   {}""".format(exception)
        raise AppError(error)

    if state == 1:

        if len(subjects) > 1:
            error = """course '{}' has errors with its desirable subjects
                       Error Details : 
                       Expected one desirable subject, found many""".format(course)
            raise AppError(error)

        return True if subjects[0] in results else False

    elif state == 2:

        for subject in results:
            if subject in subjects:
                return True

        return False

    else:
        error = """course '{}' has errors with its desirable subjects
                   Error Details : 
                   Invalid value for desirable subject, expects 1 or 2 found {}""".format(course, state)
        raise AppError(error)


def check_relevant(course, number, results):

    db_subjects = CourseSubjectsSerializer(
        CourseSubjects.objects.filter(category="relevant", course=course), many=True
    ).data

    if not db_subjects:
        error = """course '{}' has errors with its relevant subjects
                   Error Details : 
                   Doesnt have relevant subjects""".format(course)
        raise AppError(error)

    try:
        subjects = [x['subject'] for x in db_subjects]
    except KeyError as exception:
        error = """There was an error while checking subjects
                   Error Details
                   {}""".format(exception)
        raise AppError(error)

    if number == 1:

        if len(subjects) > 1:
            error = """course '{}' has errors with its relevant subjects
                       Error Details : 
                       Expected one relevant subject, found more""".format(course)
            raise AppError(error)

        return True if subjects[0] in results else False

    elif number == 2:

        if len(subjects) > 2:
            error = """course '{}' has errors with its relevant subjects
                       Error Details : 
                       Expected two relevant subject, found more""".format(course)
            raise AppError(error)

        if len(subjects) < 2:
            error = """course '{}' has errors with its relevant subjects
                       Error Details : 
                       Expected two relevant subject, found less""".format(course)
            raise AppError(error)

        count = 0

        for subject in results:
            if subject in subjects:
                count = count + 1

        return True if count == 2 else False

    else:

        error = """course '{}' has errors with its relevant subjects
                   Error Details : 
                   Number of relevant subjects is greater than 2""".format(course)
        raise AppError(error)


def check_essentials(course, number, results):

    db_subjects = CourseSubjectsSerializer(
        CourseSubjects.objects.filter(category="essential", course=course), many=True
    ).data

    if not db_subjects:
        error = """course '{}' has errors with its essential subjects
                   Error Details : 
                   Doesnt have essential subjects""".format(course)
        raise AppError(error)

    try:
        subjects = [x['subject'] for x in db_subjects]
    except KeyError as exception:
        error = """There was an error while checking subjects
                   Error Details
                   {}""".format(exception)
        raise AppError(error)

    if number == 1:

        if len(subjects) > 1:
            error = """course '{}' has errors with its essential subjects
                                   Error Details : 
                                   Expected one essential subject, found many""".format(course)
            raise AppError(error)

        return True if subjects[0] in results else False

    elif number == 2:

        if len(subjects) > 2:
            error = """course '{}' has errors with its essential subjects
                                   Error Details : 
                                   Expected two essential subjects, found more than two""".format(course)
            raise AppError(error)

        if len(subjects) < 2:
            error = """course '{}' has errors with its essential subjects
                                   Error Details : 
                                   Expected two essential subjects, found less than two""".format(course)
            raise AppError(error)

        for subject in subjects:
            if subject not in results:
                return False

        return True

    elif number == 3:

        for subject in subjects:
            if subject in results:
                return True

        return False

    else:
        error = "Number of essential subjects is greater than 2 for course code : " + course
        raise AppError(error)


def check_course_subjects(course_code, uace_results):

    course_subjects = CourseConstraintsSerializer(
        CourseConstraints.objects.filter(course=course_code), many=True
    ).data

    try:

        if course_subjects:

            if len(course_subjects) > 1:
                raise DatabaseError("has more than on entry for its essential, relevant and desirable subjects")

            course_subjects = course_subjects[0]

            no_of_essentials = course_subjects['essentials']
            no_of_relevant = course_subjects['relevant']
            desirable_state = course_subjects['desirable_state']
        else:
            raise DatabaseError("Doesn't have essential, relevant and desirable subjects")

    except (AttributeError, KeyError, TypeError, DatabaseError) as errors:
        error = """course '{}' has errors with either its essential, relevant or desirable subjects
        Error Details : 
        {}""".format(course_code, errors)

        raise AppError(error)

    essential_check = check_essentials(course_code, no_of_essentials, uace_results)
    relevant_check = check_relevant(course_code, no_of_relevant, uace_results)
    desirable_check = check_desirable(course_code, desirable_state, uace_results)

    if essential_check:
        logger.error("has essentials")
    if relevant_check:
        logger.error("has relevant")
    if desirable_check:
        logger.error("has desirable")

    if essential_check and relevant_check and desirable_check:
        return True
    else:
        return False
