import logging
logger = logging.getLogger(__name__)


def append_relevant(relevant_subjects, no_relevant, init_list):
    results = []
    combination = init_list[:]

    if no_relevant == 1:

        for subject in relevant_subjects:

            if subject not in init_list:
                combination.append(subject)
                results.append(combination)
                combination = init_list[:]

    elif no_relevant == 2:

        for index_subject in range(0, len(relevant_subjects) - 1):

            combination.append(relevant_subjects[index_subject])
            mid = combination[:]

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

    results = []
    if no_desires == 1:

        if len(desires) != 1:
            # error
            pass

        init_list.append(desires[0])
        results.append(init_list)

    else:

        combination = init_list[:]
        for d in desires:
            if ((d == "UACE_SUB_MATH") and ("UACE_MATH" in init_list)) \
                    or ((d == "UACE_SUB_COMP") and ("UACE_MATH" not in init_list)):
                continue

            combination.append(d)
            results.append(combination)
            combination = init_list[:]

    return results


def combine_subjects(essentials, relevant_subjects, desirable, desirable_state, essentials_no, relevant_no, initial_es):

    output = []
    initial = initial_es[:]

    if essentials_no == 3:

        if len(initial_es) != 1:
            # log error
            logger.error(initial_es)
            logger.error("an error in combine subjects => essentials = 3")

        relevant_no = 2
        for y in essentials:
            if y in relevant_subjects:
                relevant_subjects.remove(y)

        relevant_out = append_relevant(relevant_subjects, relevant_no, initial_es)

        for x in relevant_out:
            desirable_output = append_desirable(desirable, desirable_state, x)

            for y in desirable_output:
                output.append(y)

        for y in essentials:
            if y in relevant_subjects:
                relevant_subjects.remove(y)

        essentials_no = 2
        relevant_no = 1

    if essentials_no == 1 or (len(initial_es) == 2 and essentials_no == 2):

        relevant_output = append_relevant(relevant_subjects, relevant_no, essentials)

        for comb in relevant_output:

            desirable_output = append_desirable(desirable, desirable_state, comb)

            for x in desirable_output:
                output.append(x)

    elif essentials_no == 2:

        if len(initial_es) == 1:

            for essential in essentials:
                initial_es = initial[:]

                initial_es.append(essential)

                relevant_output = append_relevant(relevant_subjects, relevant_no, initial_es)

                for comb in relevant_output:
                    desirable_output = append_desirable(desirable, desirable_state, comb)
                    for x in desirable_output:
                        output.append(x)

        # elif len(initial_es) == 2:
        #
        #     relevant_output = append_relevant(relevant_subjects, relevant_no, initial_es)
        #
        #     for comb in relevant_output:
        #         desirable_output = append_desirable(desirable, desirable_state, comb)
        #
        #         for x in desirable_output:
        #             output.append(x)

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

        elif len(initial_es) == 3:
            # error
            desirable_output = append_desirable(desirable, desirable_state, initial_es)

            for x in desirable_output:
                output.append(x)

        else:
            # error
            pass

    else:
        # error
        pass

    return output
