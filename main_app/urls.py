from django.urls import path

from .views import course_recommendation, uace_combination, careers, uace_subjects, uce_subjects, CareersList

urlpatterns = [
    # path("careers/", careers, name="careers"),
    path("careers/", CareersList.as_view(), name="careers"),
    path("course/", course_recommendation, name="course recommendation"),
    path("combination/", uace_combination, name="uace recommendation"),
    path("uace_subjects/", uace_subjects, name="uace"),
    path("uce_subjects/", uce_subjects, name="uce"),
]
