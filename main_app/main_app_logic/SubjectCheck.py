from app_logic.AppExceptions import AppError
from main_app.models import CourseSubjects, CourseConstraints
from main_app.serializers import CourseSubjectsSerializer, CourseConstraintsSerializer
from subjects.models import UaceSubjects
from subjects.serializers import UaceOptionalsSerializer
from rest_framework.response import Response
from rest_framework import status


def check_desirable(course, state, results):
    if state == 1:
        try:
            subject = CourseSubjectsSerializer(CourseSubjects.objects.filter(category="desirable", course=course)).data

        except AttributeError:
            return Response(
                {'Message': "Essential subject expected to be one but found many"},
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return True if subject in results else False, subject

    elif state == 2:
        subjects = UaceOptionalsSerializer(UaceSubjects.objects.filter(category="optional")).data
        return True, subjects
    pass


def check_relevant(course, number, results):

    if number == 1:

        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="relevant", course=course), many=True).data

        count = 0
        for subject in results:
            if subject in subjects:
                count = count+1

        if count == 2:
            return True, subjects
        elif count < 2:
            return False, subjects
        else:
            error = "Error while computing relevant subjects for course code : " + course
            raise AppError(error)

    elif number == 2:
        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="relevant", course=course), many=True
        ).data

        count = 0
        for subject in results:
            if subject in subjects:
                count = count + 1

        if count == 1:
            return True, subjects
        elif count < 1:
            return False, subjects
        else:
            error = "Error while computing relevant subjects for course code : " + course
            raise AppError(error)

    elif number == 3:
        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="relevant", course=course), many=True
        ).data

        for subject in results:
            if subject in subjects:
                return True, subjects

        return False, subjects

    else:
        error = "Number of relevant subjects is greater than 3 for course code : " + course
        raise AppError(error)


def check_essentials(course, number, results):

    if number == 1:

        try:
            subject = CourseSubjectsSerializer(CourseSubjects.objects.filter(category="essential", course=course)).data

        except AttributeError:
            error = "Found course '{}' with many essential subjects. Expected only one".format(course)
            raise AppError(error)

        return True if subject in results else False, subject

    elif number == 2:
        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="essential", course=course), many=True
        ).data

        for subject in subjects:
            if subject not in results:
                return False, subjects

        return True, subjects

    elif number == 3:
        subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(category="essential", course=course), many=True
        ).data

        for subject in subjects:
            if subject in results:
                return True, subjects

        return False, subjects

    else:
        error = "Number of essential subjects is greater than 3 for course code : " + course
        raise AppError(error)


def check_course_subjects(course_code, uace_results):

    try:
        course_subjects = CourseConstraintsSerializer(CourseConstraints.objects.filter(course=course_code))

        no_of_essentials = course_subjects['essentials']
        no_of_relevant = course_subjects['relevant']
        desirable_state = course_subjects['desirable_state']

    except (AttributeError, KeyError):
        error = "course '{}' has errors with or lucks essential, relevant and desirable subjects".format(course_code)
        raise AppError(error)

    essential_check = check_essentials(course_code, no_of_essentials, uace_results)
    relevant_check = check_relevant(course_code, no_of_essentials, uace_results)
    desirable_check = check_desirable(course_code, desirable_state, uace_results)

    if essential_check and relevant_check and desirable_check:

        return True
    else:
        return False
