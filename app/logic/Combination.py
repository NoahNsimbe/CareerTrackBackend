from rest_framework import status
from rest_framework.response import Response

from app.logic.AppExceptions import AppError, DatabaseError
from app.logic.ConstraintCheck import check_o_level
from app.models import CareerCourses, CourseConstraints, CourseSubjects, UaceSubjects
from app.serializers import CareerCoursesSerializer, CourseConstraintsSerializer, CourseSubjectsSerializer, \
    UaceSerializer
import itertools
from app.logic.Combine import combine_subjects


def get_combination(career, uce_results):
    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=str(career).strip()), many=True).data

    if career_courses:

        combinations = []

        course_list = [x["course"] for x in career_courses]

        for course_code in course_list:

            try:

                if len(uce_results) == 0:
                    fn_output = generate_combination(course_code)
                    for x in fn_output:
                        combinations.append(x)
                else:
                    if check_o_level(course_code, uce_results):

                        combination = generate_combination(course_code)

                        for x in combination:
                            combinations.append(x)

            except AppError as exception:

                print("Exception Has occurred : \n{} ".format(exception))

                errors = "Sorry, there was an error while processing information for the career '{}'".format(career)

                return False, None, errors

        output = make_output(combinations)

        return True, output, None

    else:
        errors = "Sorry, we haven't yet updated our system to cater for '{}'".format(career)
        print(errors)

        return False, None, errors


def get_subjects(essentials, relevant):
    if essentials[0] == "UACE_ALL_SCIENCES" and relevant[0] == "UACE_ALL_SCIENCES":
        subjects = UaceSerializer(
            UaceSubjects.objects.filter(category="Sciences"), many=True
        ).data
        relevant = essentials = [x["code"] for x in subjects]

    elif essentials[0] == "UACE_ALL_ARTS" and relevant[0] == "UACE_ALL_ARTS":
        subjects = UaceSerializer(
            UaceSubjects.objects.filter(category="Arts"), many=True
        ).data
        relevant = essentials = [x["code"] for x in subjects]

    elif essentials[0] == "UACE_ALL_SCIENCES" and relevant[0] == "UACE_ALL_ARTS":
        subjects = UaceSerializer(
            UaceSubjects.objects.filter(category="Sciences"), many=True
        ).data
        essentials = [x["code"] for x in subjects]

        subjects = UaceSerializer(
            UaceSubjects.objects.filter(category="Arts"), many=True
        ).data
        relevant = [x["code"] for x in subjects]

    elif essentials[0] == "UACE_ALL_ARTS" and relevant[0] == "UACE_ALL_SCIENCES":
        subjects = UaceSerializer(
            UaceSubjects.objects.filter(category="Arts"), many=True
        ).data
        essentials = [x["code"] for x in subjects]

        subjects = UaceSerializer(
            UaceSubjects.objects.filter(category="Sciences"), many=True
        ).data
        relevant = [x["code"] for x in subjects]

    elif essentials[0] == "UACE_ALL_SCIENCES" and relevant[0] == "UACE_ALL":
        subjects = UaceSerializer(
            UaceSubjects.objects.filter(category="Sciences"), many=True
        ).data
        essentials = [x["code"] for x in subjects]

        subjects = UaceSerializer(
            UaceSubjects.objects.all().exclude(category="Category").exclude(category="Subsidiary"),
            many=True
        ).data
        relevant = [x["code"] for x in subjects]

    elif essentials[0] == "UACE_ALL_ARTS" and relevant[0] == "UACE_ALL":
        subjects = UaceSerializer(
            UaceSubjects.objects.filter(category="Arts"), many=True
        ).data
        essentials = [x["code"] for x in subjects]

        subjects = UaceSerializer(
            UaceSubjects.objects.all().exclude(category="Category").exclude(category="Subsidiary"),
            many=True
        ).data
        relevant = [x["code"] for x in subjects]

    else:
        subjects = UaceSerializer(
            UaceSubjects.objects.all().exclude(category="Category").exclude(category="Subsidiary"),
            many=True
        ).data

        relevant = essentials = [x["code"] for x in subjects]

    return essentials, relevant


def get_all(category):
    check_all = category[:]

    for code in check_all:
        if str(code) == "UACE_ALL_LANG":
            subject_codes = UaceSerializer(
                UaceSubjects.objects.filter(language_subject=True), many=True
            ).data
        elif str(code) == "UACE_ALL_SCIENCES":
            subject_codes = UaceSerializer(
                UaceSubjects.objects.filter(category="Sciences"), many=True
            ).data
        elif str(code) == "UACE_ALL":
            subject_codes = UaceSerializer(
                UaceSubjects.objects.all().exclude(category="Category").exclude(category="Subsidiary"),
                many=True
            ).data
        elif str(code) == "UACE_ALL_ARTS":
            subject_codes = UaceSerializer(
                UaceSubjects.objects.filter(category="Arts"), many=True
            ).data
        else:
            subject_codes = []

        if len(subject_codes) != 0:

            if code in category:
                category.remove(code)

            for subject_code in subject_codes:
                category.append(subject_code["code"])

    return category


def generate_combination(course):
    try:

        course_subjects = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(course=course), many=True
        ).data

        course_constraints = CourseConstraintsSerializer(
            CourseConstraints.objects.filter(course=course), many=True
        ).data

        if course_subjects and course_constraints:

            if len(course_constraints) > 1:
                raise DatabaseError("has more than on entry for its essential, relevant and desirable subjects")
            else:
                course_constraints = course_constraints[0]

            no_of_essentials = int(course_constraints['essentials'])
            no_of_relevant = int(course_constraints['relevant'])
            desirable_state = int(course_constraints['desirable_state'])
            all_subjects = course_constraints['all_subjects']
            a_level_constraint = course_constraints['a_level_constraint']

            essentials = [x["subject"] for x in course_subjects if x["category"] == "essential"]
            relevant = [x["subject"] for x in course_subjects if x["category"] == "relevant"]
            desirable = [x["subject"] for x in course_subjects
                         if x["category"] == "desirable"]
            comp = []

            if all_subjects:
                essentials, relevant = get_subjects(essentials, relevant)

            else:

                relevant = get_all(relevant)
                essentials = get_all(essentials)

                if a_level_constraint:
                    for x in course_subjects:
                        if (x["category"] == "essential") and x["compulsory_state"]:
                            comp.append(x["subject"])
                            if x["subject"] in essentials:
                                essentials.remove(x["subject"])
                    if len(essentials) == 0:
                        essentials = comp[:]

            relevant = list(set(relevant))
            essentials = list(set(essentials))

            if len(relevant) == 0 or len(essentials) == 0 or len(desirable) == 0:
                raise DatabaseError("Doesn't have either essential, relevant or desirable subjects or lucks all.")

        else:
            raise DatabaseError("Doesn't have either essential, relevant or desirable subjects or lucks all")

    except Exception as errors:
        error = """course '{}' has errors with either its essential, relevant or desirable subjects
           Error Details :
           Function => generate_combination in Combination.py
           {}""".format(course, errors)

        raise AppError(error)

    results = combine_subjects(
        essentials, relevant, desirable, desirable_state, no_of_essentials, no_of_relevant, comp)

    return results


def make_output(results):
    # add error handling

    recommendation = []
    try:

        results.sort()
        cleaned_results = list(results for results, _ in itertools.groupby(results))

        for result in cleaned_results:

            combination_subjects = []
            abbreviation = str()
            combination = dict()

            for sub in result:
                subjects = UaceSerializer(UaceSubjects.objects.filter(code=sub), many=True).data[0]

                if subjects["category"] == "Subsidiary":
                    abbreviation = abbreviation + "/"

                abbreviation = abbreviation + str(subjects["abbr"])

                combination_subjects.append(subjects["name"])

            combination_subjects.append("General Paper")

            subjects_abbr = abbreviation + " and General Paper"

            combination["abbreviation"] = subjects_abbr
            combination["subjects"] = combination_subjects
            recommendation.append(combination)

    except Exception as errors:

        error = """Error occurred while making output for {}
           Error Details :
           Function => make_output in Combination.py
           {}""".format(results, errors)

        raise AppError(error)
    return recommendation


def uace_combination(data):
    career = data.get("career")
    uce_results = data.get("uce_results", None)

    if uce_results is None:
        success, results, errors = get_combination(career, [])

    else:
        career = str(career).strip()
        success, results, errors = get_combination(career, uce_results)

    if success:
        return Response(results, status.HTTP_200_OK)

    else:
        response = {'Message': errors}
        return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


def combination_recommendation(program_code):

    combinations = []

    try:
        fn_output = generate_combination(program_code)
        for x in fn_output:
            combinations.append(x)

    except Exception as exception:

        print("Exception Has occurred : \n{} ".format(exception))

        print("Exception Has occurred: \n {}".format(exception))
        raise Exception("Error occurred while processing recommended combinations for program code {}".format(program_code))

    output = make_output(combinations)

    return output
