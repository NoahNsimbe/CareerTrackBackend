from django.urls import path

from .views import course_recommendation, uace_combination, CareersList, UceList, UaceList

urlpatterns = [
    path("careers/", CareersList.as_view(), name="careers"),
    path("course/", course_recommendation, name="course recommendation"),
    path("combination/", uace_combination, name="uace recommendation"),
    path("uace_subjects/", UaceList.as_view(), name="uace"),
    path("uce_subjects/", UceList.as_view(), name="uce"),
]
