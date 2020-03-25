def check_alevel(course, results):
    return True


def check_olevel(course, results):
    return True


def check_course_constraints(course_code, uace_results):

    alevel_constraint_check = check_alevel(course_code, uace_results)
    olevel_constraint_check = check_olevel(course_code, uace_results)

    if alevel_constraint_check and olevel_constraint_check:
        return True
    else:
        return False
