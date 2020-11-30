from app.models import Courses, AppRequests, OLevelConstraints, CutOffPoints, CourseConstraints, CourseSubjects, \
    ALevelConstraints
from app.serializers import CourseSerializer, OLevelConstraintSerializer, CutOffPointsSerializer, \
    CourseConstraintsSerializer, CourseSubjectsSerializer, ALevelConstraintSerializer, ProgramDetailsSerializer


class Program:
    uce_results = dict({})
    program_code = None
    uace_results = dict({})
    requestType = None

    def __init__(self, program_code, uce_results=None, uace_results=None):
        self.uce_results = uce_results
        self.program_code = program_code
        self.uace_results = uace_results

    def get_constraints(self):
        self.program_code = CourseSerializer(Courses.objects.filter(code=self.program_code)).data

        if self.program_code is None or self.program_code == []:
            return "error"

        print(self.program_code)

        constraints = OLevelConstraintSerializer(OLevelConstraints.objects.filter(code=self.program_code), many=True).data

        print(constraints)

    def get_details(self):

        details = dict({
            'program': {},
            'cut_off_points': {},
            'program_constraints': {},
            'program_subjects': {},
            'a_level_constraints': {},
            'o_level_constraints': {}
        })

        details['program'] = CourseSerializer(Courses.objects.get(code=self.program_code)).data

        details['cut_off_points'] = CutOffPointsSerializer(
            CutOffPoints.objects.filter(course__code__exact=self.program_code), many=True).data

        details['program_constraints'] = CourseConstraintsSerializer(
            CourseConstraints.objects.filter(course__code__exact=self.program_code), many=True).data

        details['program_subjects'] = CourseSubjectsSerializer(
            CourseSubjects.objects.filter(course__code__exact=self.program_code), many=True).data

        details['a_level_constraints'] = ALevelConstraintSerializer(
            ALevelConstraints.objects.filter(code__exact=self.program_code), many=True).data

        details['o_level_constraints'] = OLevelConstraintSerializer(
            OLevelConstraints.objects.filter(code__exact=self.program_code), many=True).data

        # print(details['program_subjects'])
        # program_details_serializer = ProgramDetailsSerializer(data=details)
        # program_details_serializer.is_valid(raise_exception=True)
        # return program_details_serializer.data

        return details


