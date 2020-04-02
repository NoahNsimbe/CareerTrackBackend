from app_logic.AppExceptions import AppError, DatabaseError
from subjects.models import UaceSubjects
from subjects.serializers import UaceSerializer
from .ConstraintCheck import check_o_level
from main_app.models import CareerCourses, CourseConstraints, CourseSubjects
from main_app.serializers import CareerCoursesSerializer, CourseConstraintsSerializer, CourseSubjectsSerializer

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
            subject_constraint = course_constraints['subject_constraint']

            # logger.error(course_subjects)

            essentials = [x["subject"] for x in course_subjects if x["category"] == "essential"]
            relevant = [x["subject"] for x in course_subjects if x["category"] == "relevant"]
            desirable = [x["subject"] for x in course_subjects if x["category"] == "desirable"]

            # logger.error("am here")

        else:
            raise DatabaseError("Doesn't have essential, relevant and desirable subjects")

    except (AttributeError, KeyError, TypeError, ValueError, DatabaseError) as errors:
        error = """course '{}' has errors with either its essential, relevant or desirable subjects
           Error Details : 
           Function => generate_combination in Combination.py
           {}""".format(course, errors)

        raise AppError(error)

    if all_subjects == "True":

        subjects = UaceSerializer(UaceSubjects.objects.all(), many=True).data
        results = dict({"All A level subjects": subjects})

    else:

        if subject_constraint == "True":
            comp = [x["subject"] for x in course_subjects
                    if x["category"] == "essential" and x["compulsory_state"] == "True"
                    ]
            results = combine_subjects(
                essentials, relevant, desirable, desirable_state, no_of_essentials, no_of_relevant, comp)

        else:
            results = combine_subjects(
                essentials, relevant, desirable, desirable_state, no_of_essentials, no_of_relevant, [])

    return results


def make_output(results):

    recommendation = dict()

    for result in results:

        combination = []
        abbreviate = str()

        for sub in result:
            subjects = UaceSerializer(UaceSubjects.objects.filter(code=sub), many=True).data[0]

            if subjects["category"] == "Subsidiary":
                abbreviate = abbreviate + "/"

            abbreviate = abbreviate + str(subjects["abbr"])

            combination.append(subjects["name"])

        if abbreviate not in recommendation:
            abbreviate = abbreviate + " and General Paper"
            recommendation[abbreviate] = combination
        else:
            abbreviate = abbreviate + " & General Paper"
            recommendation[abbreviate.lower()] = combination

    return recommendation


def combine_subjects(essentials, relevant_subjects, desirable, desirable_state, essentials_no, relevant_no, initial_es):

    def append_relevant(relevantsubjects, no_relevant, init_list):
        results = []
        combination = init_list

        if no_relevant == 1:

            for subject in relevantsubjects:
                combination.append(subject)
                results.append(combination)
                combination = init_list

        elif no_relevant == 2:

            for index_subject in range(0, len(relevantsubjects) - 1):

                mid = combination.append(relevantsubjects[index_subject])

                for index_subject2 in range(index_subject + 1, len(relevantsubjects)):

                    combination.append(relevantsubjects[index_subject2])
                    results.append(combination)
                    combination = mid

                combination = init_list
        else:
            # error, number of relevant is more than 2
            pass

        return results

    def append_desirable(desires, no_desires, init_list):

        results = []
        combination = init_list

        if no_desires == 1:
            init_list.append(desires[0])
            return init_list

        else:
            for d in desires:
                if d == "UACE_SUB_MATH" and "UACE_MATH" in init_list:
                    continue

                combination.append(d)
                results.append(combination)
                combination = init_list

            return results

    output = []

    if essentials_no == 1:
        if relevant_no != 2:
            # an error
            return

        relevant_output = append_relevant(relevant_subjects, relevant_no, essentials)

        for comb in relevant_output:

            output.append(append_desirable(desirable, desirable_state, comb))

    elif essentials_no == 2:
        if relevant_no != 1:
            # an error
            return

        if len(initial_es) == 1:

            for essential in essentials:
                initial_es.append(essential)
                relevant_output = append_relevant(relevant_subjects, relevant_no, essential)

                for comb in relevant_output:
                    output.append(append_desirable(desirable, desirable_state, comb))

        elif len(initial_es) == 2:
            relevant_output = append_relevant(relevant_subjects, relevant_no, initial_es)

            for comb in relevant_output:
                output.append(append_desirable(desirable, desirable_state, comb))

        elif len(initial_es) == 0:

            for index in range(0, len(essentials)-1):

                combinations = [essentials[index]]

                for second_index in range(index+1, len(essentials)):

                    combinations.append(essentials[second_index])

                    relevant_output = append_relevant(relevant_subjects, relevant_no, combinations)

                    for comb in relevant_output:

                        desirable_output = append_desirable(desirable, desirable_state, comb)

                        output.append(desirable_output)

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

                if check_o_level(course_code, uce_results, False):

                    fn_output = generate_combination(course_code)
                    for x in fn_output:
                        combinations.append(x)

            except (AppError, KeyError, AttributeError) as exception:

                logger.error("Exception Has occurred : \n " + exception.message)

                errors = "Sorry, there was an error while processing information for the career '{}'".format(career)

                return False, None, errors

        # logger.error("combinations")
        # logger.error(combinations)
        output = make_output(combinations)

        return True, output, None

    else:
        errors = "Sorry, we haven't yet updated our system to cater for {}".format(career)
        logger.error(errors)
        return False, None, errors
