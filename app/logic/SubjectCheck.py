from app.logic.AppExceptions import AppError, DatabaseError
from app.logic.Combination import get_all
from app.models import CourseSubjects, CourseConstraints
from app.serializers import CourseSubjectsSerializer, CourseConstraintsSerializer


def check_desirable(course, state, subjects, results):

    # db_subjects = CourseSubjectsSerializer(
    #     CourseSubjects.objects.filter(category="desirable", course=course), many=True
    # ).data
    #
    # if not db_subjects:
    #     error = """course '{}' has errors with its desirable subjects
    #                Error Details :
    #                Doesnt have desirable subjects : Table => CourseSubjects""".format(course)
    #     raise AppError(error)
    #
    # try:
    #     subjects = [x['subject'] for x in db_subjects]
    # except KeyError as exception:
    #     error = """There was an error while checking subjects
    #                Error Details
    #                {}""".format(exception)
    #     raise AppError(error)

    if state == 1:

        if len(subjects) > 1:
            error = """course '{}' has errors with its desirable subjects
                       Error Details : 
                       Expected one desirable subject, found many : Table => CourseSubjects""".format(course)
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
                   Invalid value for desirable subject, expects 1 or 2 found {} : Table => CourseSubjects"""\
            .format(course, state)
        raise AppError(error)


def check_relevant(course, number, subjects, results, essentials):

    if number == 3:
        if check_essentials(course, 2, essentials, results, False):
            number = 1
        else:
            number = 2

    if number == 1:

        for subject in subjects:
            if subject in results:
                return True

        return False

    elif number == 2:

        if len(subjects) < 2:
            error = """course '{}' has errors with its relevant subjects
                       Error Details : 
                       Expected two relevant subject, found less : Table => CourseSubjects""".format(course)
            raise AppError(error)

        count = 0

        for subject in results:
            if subject in subjects:
                count = count + 1

        return True if count == 2 else False

    else:
        error = """course '{}' has errors with its relevant subjects
                   Error Details : 
                   Number of relevant subjects is greater than 2 : Table => CourseSubjects""".format(course)
        raise AppError(error)


def check_essentials(course, number, subjects, results, subject_constrained):

    if subject_constrained:
        compulsory_subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="essential", compulsory_state=True, course=course), many=True
        ).data

        if not compulsory_subjects:
            error = """There was an error while checking course subjects for {}
                       Error Details
                       Missing compulsory UACE subjects yet its subject constrained : Table => CourseSubjects"""\
                .format(course)
            raise AppError(error)

        for x in compulsory_subjects:
            if x['subject'] not in results:
                return False

    # db_subjects = CourseSubjectsSerializer(
    #     CourseSubjects.objects.filter(category="essential", course=course), many=True
    # ).data
    #
    # if not db_subjects:
    #     error = """course '{}' has errors with its essential subjects
    #                Error Details :
    #                Doesnt have essential subjects : Table => CourseSubjects""".format(course)
    #     raise AppError(error)
    #
    # try:
    #     subjects = [x['subject'] for x in db_subjects]
    # except KeyError as exception:
    #     error = """There was an error while checking subjects
    #                Error Details
    #                {} : Table => CourseSubjects""".format(exception)
    #     raise AppError(error)

    if number == 1 or number == 3:

        # if len(subjects) > 1:
        #     error = """course '{}' has errors with its essential subjects
        #                Error Details :
        #                Expected one essential subject, found many : Table => CourseSubjects"""\
        #         .format(course)
        #     raise AppError(error)

        for subject in subjects:
            if subject in results:
                return True

        return False

    elif number == 2:

        if len(subjects) < 2:
            error = """course '{}' has errors with its essential subjects
                       Error Details : 
                       Expected at least two essential subjects, found less : Table => CourseSubjects""".format(course)
            raise AppError(error)

        count = 0

        for subject in results:
            if subject in subjects:
                count = count + 1

        return True if count >= 2 else False

    else:
        error = "Number of essential subjects is greater than 2 for course code : {} : Table => CourseSubjects"\
                .format(course)
        raise AppError(error)


def check_subject(course_code, uace_results):

    course_constraints = CourseConstraintsSerializer(
        CourseConstraints.objects.filter(course=course_code), many=True
    ).data

    course_subjects = CourseSubjectsSerializer(
        CourseSubjects.objects.filter(course=course_code), many=True
    ).data

    try:

        if course_constraints:

            if len(course_constraints) > 1:
                raise DatabaseError("has more than one entry for its essential, relevant and desirable subjects")
            else:
                course_constraints = course_constraints[0]

            if not course_subjects:
                raise DatabaseError("Does not have course subjects")

            essential = list()
            relevant = list()
            desirable = list()

            for subject in course_subjects:

                if str(subject["category"]).upper() == "ESSENTIAL":
                    essential.append(subject['subject'])

                elif str(subject["category"]).upper() == "RELEVANT":
                    relevant.append(subject['subject'])

                elif str(subject["category"]).upper() == "DESIRABLE":
                    desirable.append(subject['subject'])

                else:
                    pass

            if not(any(relevant) and any(essential) and any(desirable)):
                raise DatabaseError("Does not have either essential, relevant or desirable subjects")

            no_of_essentials = course_constraints['essentials']
            no_of_relevant = course_constraints['relevant']
            desirable_state = course_constraints['desirable_state']
            all_subjects = course_constraints['all_subjects']
            a_level_constraint = course_constraints['a_level_constraint']

        else:
            raise DatabaseError("Doesn't have constraints")

    except Exception as errors:
        error = """
        course '{}' has errors with either its essential, relevant or desirable subjects
        Error Details : 
        {}""".format(course_code, errors)

        raise AppError(error)

    if all_subjects:
        if a_level_constraint:
            essential_check = relevant_check = desirable_check = True
        else:
            essential_check = relevant_check = desirable_check = True
    else:
        relevant = get_all(relevant)
        essential = get_all(essential)

        essential_check = check_essentials(course_code, no_of_essentials, essential, uace_results, a_level_constraint)
        relevant_check = check_relevant(course_code, no_of_relevant, relevant, uace_results, essential)
        desirable_check = check_desirable(course_code, desirable_state, desirable, uace_results)

    db_subjects = dict({"essential": essential, "relevant": relevant, "desirable": desirable})

    if essential_check and relevant_check and desirable_check:
        return True, db_subjects
    else:
        return False, db_subjects
