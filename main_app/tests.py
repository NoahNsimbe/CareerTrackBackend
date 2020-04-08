import json
import os

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from career_track.settings import BASE_DIR
from main_app.models import Careers, Courses, CareerCourses


class CombinationTestCase(APITestCase):
    fixtures = ['dump.json']
    url = reverse('uace recommendation')

    data_path = os.path.join(BASE_DIR, "api.json")
    input_test_data = json.load(open(data_path))

    # def setUp(self):
    #     pass

    # @classmethod
    # def setUpTestData(cls):
    #
    #     cls.careers = Careers.objects.create(name="Doctor", description="Treats people")
    #     cls.courses = Courses.objects.create(code="MAM", name="Medicine", description="Medicine")
    #     cls.career_courses = CareerCourses.objects.create(career="Doctor", course="MAM")
    #
    #     cls.careers = Careers.objects.create(name="Doctor", description="Treats people")
    #     cls.careers = Careers.objects.create(name="Doctor", description="Treats people")

    def test_without_results(self):

        data = self.input_test_data["combination"]["without"]

        success = self.client.post(self.url, data["available"], format='json')
        server_error = self.client.post(self.url, data["unavailable"], format='json')
        missing_data = self.client.post(self.url, data["no_career"], format='json')

        self.assertEqual(success.status_code, status.HTTP_200_OK)
        self.assertEqual(missing_data.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(server_error.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def test_with_results(self):
    #
    #     data = dict({
    #         "no_career": {"jj": "Doctor"},
    #         "available": {"career": "Doctor"},
    #         "unavailable": {"career": "XX"},
    #     })
    #
    #     success = self.client.post(self.url, data["available"], format='json')
    #     server_error = self.client.post(self.url, data["unavailable"], format='json')
    #     missing_data = self.client.post(self.url, data["no_career"], format='json')
    #
    #     self.assertEqual(success.status_code, status.HTTP_200_OK)
    #     self.assertEqual(missing_data.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(server_error.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
