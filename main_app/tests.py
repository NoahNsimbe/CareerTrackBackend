import json
import os
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from career_track.settings import BASE_DIR
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault('SECRET_KEY', 'testing')


class InfoTestCase(APITestCase):

    fixtures = ['dump.json']
    careers_url = reverse('careers')
    uace_url = reverse('uace')
    uce_url = reverse('uce')

    def test_careers(self):
        logger.error(os.getenv("SECRET_KEY"))
        resp = self.client.get(self.careers_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_subjects(self):

        uce_resp = self.client.get(self.uce_url)
        self.assertEqual(uce_resp.status_code, status.HTTP_200_OK)

        uace_resp = self.client.get(self.uace_url)
        self.assertEqual(uace_resp.status_code, status.HTTP_200_OK)

# class CombinationTestCase(APITestCase):
#
#     fixtures = ['dump.json']
#     data_path = os.path.join(BASE_DIR, "api.json")
#     input_test_data = json.load(open(data_path))
#     url = reverse('uace recommendation')
#     without_data = input_test_data["combination"]["without"]
#     with_data = input_test_data["combination"]["with"]
#
#     def test_without_results(self):
#
#         success = self.client.post(self.url, self.without_data["available"], format='json')
#         self.assertEqual(success.status_code, status.HTTP_200_OK)
#
#         server_error = self.client.post(self.url, self.without_data["unavailable"], format='json')
#         missing_data = self.client.post(self.url, self.without_data["no_career"], format='json')
#         # empty = self.client.post(self.url, self.without_data["empty"], format='json')
#
#         self.assertEqual(missing_data.status_code, status.HTTP_400_BAD_REQUEST)
#         # self.assertEqual(empty.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(server_error.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def test_with_results(self):
#
#         o_level_fail = self.client.post(self.url, self.with_data["o_level_fail"], format='json')
#         o_level_pass = self.client.post(self.url, self.with_data["o_level_pass"], format='json')
#         one_mandatory_pass = self.client.post(self.url, self.with_data["one_mandatory_pass"], format='json')
#         one_mandatory_fail = self.client.post(self.url, self.with_data["one_mandatory_fail"], format='json')
#         two_mandatory_pass = self.client.post(self.url, self.with_data["two_mandatory_pass"], format='json')
#         two_mandatory_fail = self.client.post(self.url, self.with_data["two_mandatory_fail"], format='json')
#
#         self.assertEqual(o_level_fail.status_code, status.HTTP_200_OK)
#         self.assertEqual(o_level_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(one_mandatory_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(one_mandatory_fail.status_code, status.HTTP_200_OK)
#         self.assertEqual(two_mandatory_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(two_mandatory_fail.status_code, status.HTTP_200_OK)
#
#
# class CourseTestCase(APITestCase):
#
#     fixtures = ['dump.json']
#     data_path = os.path.join(BASE_DIR, "api.json")
#     input_test_data = json.load(open(data_path))
#
#     url = reverse('course recommendation')
#     without_data = input_test_data["course"]["without"]
#     with_data = input_test_data["course"]["with"]
#
#     def test_without_results(self):
#
#         success = self.client.post(self.url, self.without_data["available"], format='json')
#         server_error = self.client.post(self.url, self.without_data["unavailable"], format='json')
#         missing_data = self.client.post(self.url, self.without_data["no_career"], format='json')
#         empty = self.client.post(self.url, self.without_data["empty"], format='json')
#
#         self.assertEqual(success.status_code, status.HTTP_200_OK)
#         self.assertEqual(missing_data.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(empty.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(server_error.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def test_with_results(self):
#
#         a_level_pass = self.client.post(self.url, self.with_data["a_level_pass"], format='json')
#         a_level_fail = self.client.post(self.url, self.with_data["a_level_fail"], format='json')
#         one_mandatory_pass = self.client.post(self.url, self.with_data["one_mandatory_pass"], format='json')
#         one_mandatory_fail = self.client.post(self.url, self.with_data["one_mandatory_fail"], format='json')
#         two_mandatory_pass = self.client.post(self.url, self.with_data["two_mandatory_pass"], format='json')
#         two_mandatory_fail = self.client.post(self.url, self.with_data["two_mandatory_fail"], format='json')
#         one_or_two_pass = self.client.post(self.url, self.with_data["one_or_two_pass"], format='json')
#         one_or_two_fail = self.client.post(self.url, self.with_data["one_or_two_fail"], format='json')
#
# #         a_level_constraint_pass = self.client.post(self.url, self.with_data["a_level_constraint_pass"], format='json')
# #         a_level_constraint_fail = self.client.post(self.url, self.with_data["a_level_constraint_fail"], format='json')
#         desirable_pass = self.client.post(self.url, self.with_data["desirable_pass"], format='json')
#         desirable_fail = self.client.post(self.url, self.with_data["desirable_fail"], format='json')
#         languages_pass = self.client.post(self.url, self.with_data["languages_pass"], format='json')
#         languages_fail = self.client.post(self.url, self.with_data["languages_fail"], format='json')
#         mandatory_many_pass = self.client.post(self.url, self.with_data["mandatory_many_pass"], format='json')
#         mandatory_many_fail = self.client.post(self.url, self.with_data["mandatory_many_fail"], format='json')
#         all_pass = self.client.post(self.url, self.with_data["all_pass"], format='json')
#         all_fail = self.client.post(self.url, self.with_data["all_fail"], format='json')
#
#         self.assertEqual(a_level_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(a_level_fail.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(one_mandatory_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(one_mandatory_fail.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(two_mandatory_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(two_mandatory_fail.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(one_or_two_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(one_or_two_fail.status_code, status.HTTP_200_OK)
#
# #         self.assertEqual(a_level_constraint_pass.status_code, status.HTTP_200_OK)
# #         self.assertEqual(a_level_constraint_fail.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(desirable_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(desirable_fail.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(languages_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(languages_fail.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(mandatory_many_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(mandatory_many_fail.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(all_pass.status_code, status.HTTP_200_OK)
#         self.assertEqual(all_fail.status_code, status.HTTP_200_OK)
