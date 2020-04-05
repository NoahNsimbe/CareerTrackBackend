from app_logic.AppExceptions import AppError, DatabaseError
from subjects.models import UaceSubjects
from subjects.serializers import UaceSerializer
from .ConstraintCheck import check_o_level
from main_app.models import CareerCourses, CourseConstraints, CourseSubjects
from main_app.serializers import CareerCoursesSerializer, CourseConstraintsSerializer, CourseSubjectsSerializer
import itertools

import logging
logger = logging.getLogger(__name__)


def combination_without_results(career):

    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data

    if career_courses:

        combinations = []

        course_list = [x["course"] for x in career_courses]

        for course_code in course_list:

            try:

                fn_output = generate_combination(course_code)
                for x in fn_output:
                    combinations.append(x)

            except (AppError, KeyError, AttributeError) as exception:

                logger.error("Exception Has occurred : \n " + exception.message)

                errors = "Sorry, there was an error while processing information for the career '{}'".format(career)

                return False, None, errors

        output = make_output(combinations)

        return True, output, None

    else:
        errors = "Sorry, we haven't yet updated our system to cater for '{}'".format(career)
        logger.error(errors)

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
            UaceSubjects.objects.filter(category="Arts"), many=True
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
            desirable = [x["subject"] for x in course_subjects if x["category"] == "desirable"]
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

            relevant = list(set(relevant))
            essentials = list(set(essentials))

            if len(relevant) == 0 or len(essentials) == 0 or len(desirable) == 0:
                raise DatabaseError("Doesn't have either essential, relevant or desirable subjects or lucks all")

        else:
            raise DatabaseError("Doesn't have either essential, relevant or desirable subjects or lucks all")

    except (AttributeError, KeyError, TypeError, ValueError, DatabaseError) as errors:
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

    recommendation = dict()

    results.sort()
    cleaned_results = list(results for results, _ in itertools.groupby(results))

    for result in cleaned_results:

        combination = []
        abbreviate = str()

        for sub in result:
            subjects = UaceSerializer(UaceSubjects.objects.filter(code=sub), many=True).data[0]

            if subjects["category"] == "Subsidiary":
                abbreviate = abbreviate + "/"

            abbreviate = abbreviate + str(subjects["abbr"])

            combination.append(subjects["name"])

        subjects_abbr = abbreviate + " and General Paper"

        if subjects_abbr not in recommendation.keys():
            recommendation[subjects_abbr] = combination
        else:
            subjects_abbr = abbreviate + " & General Paper"
            recommendation[subjects_abbr] = combination

    return recommendation


def append_relevant(relevant_subjects, no_relevant, init_list):
    results = []
    combination = []

    if no_relevant == 1:

        for subject in relevant_subjects:

            if subject not in init_list:
                combination = init_list[:]
                combination.append(subject)
                results.append(combination)

    elif no_relevant == 2:

        for index_subject in range(0, len(relevant_subjects) - 1):

            mid = combination.append(relevant_subjects[index_subject])

            for index_subject2 in range(index_subject + 1, len(relevant_subjects)):
                combination.append(relevant_subjects[index_subject2])
                results.append(combination)
                combination = mid[:]

            combination = init_list[:]
    else:
        # error, number of relevant is more than 2
        pass

    return results


def append_desirable(desires, no_desires, init_list):

    if no_desires == 1:

        if len(desires) != 0:
            #error
            return init_list

        init_list.append(desires[0])
        return init_list

    else:
        results = []
        combination = init_list[:]
        for d in desires:
            if ((d == "UACE_SUB_MATH") and ("UACE_MATH" in init_list)) \
                    or ((d == "UACE_SUB_COMP") and ("UACE_MATH" not in init_list)):
                continue

            combination.append(d)
            results.append(combination)
            combination = init_list[:]

        if len(results) == 1:
            results = results[0]

        return results


def combine_subjects(essentials, relevant_subjects, desirable, desirable_state, essentials_no, relevant_no, initial_es):

    output = []

    if essentials_no == 1:

        relevant_output = append_relevant(relevant_subjects, relevant_no, essentials)

        for comb in relevant_output:

            output.append(append_desirable(desirable, desirable_state, comb))

    elif essentials_no == 2:
        if relevant_no != 1:
            # an error
            return

        if len(initial_es) == 1:

            initial = initial_es[:]

            for essential in essentials:
                initial_es = initial[:]

                initial_es.append(essential)

                relevant_output = append_relevant(relevant_subjects, relevant_no, initial_es)

                for comb in relevant_output:
                    output.append(append_desirable(desirable, desirable_state, comb))

        elif len(initial_es) == 2:

            relevant_output = append_relevant(relevant_subjects, relevant_no, initial_es)

            for comb in relevant_output:
                output.append(append_desirable(desirable, desirable_state, comb))

        elif len(initial_es) == 0:

            for index in range(0, len(essentials)-1):

                first_sub = essentials[index]

                for second_index in range(index+1, len(essentials)):

                    combinations = [first_sub, essentials[second_index]]

                    relevant_output = append_relevant(relevant_subjects, relevant_no, combinations)

                    for comb in relevant_output:

                        desirable_output = append_desirable(desirable, desirable_state, comb)

                        for x in desirable_output:
                            output.append(x)

    else:
        # error
        pass

    return output


def combination_with_results(career, uce_results):

    career_courses = CareerCoursesSerializer(CareerCourses.objects.filter(career=career), many=True).data

    if career_courses:

        combinations = []

        course_list = [x["course"] for x in career_courses]

        for course_code in course_list:

            try:

                if check_o_level(course_code, uce_results):

                    combination = generate_combination(course_code)

                    for x in combination:

                        combinations.append(x)

            except (AppError, KeyError, AttributeError) as exception:

                logger.error("Exception Has occurred : \n {}".format(exception))

                errors = "Sorry, there was an error while processing information for the career '{}'".format(career)

                return False, None, errors

        output = make_output(combinations)

        return True, output, None

    else:
        errors = "Sorry, we haven't yet updated our system to cater for {}".format(career)
        logger.error(errors)
        return False, None, errors
