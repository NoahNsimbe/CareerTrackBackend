from django.urls import path
from .views import course_recommendation, uace_combination, get_careers, uace_subjects, uce_subjects

urlpatterns = [
    path("careers/", get_careers, name="careers"),
    path("course/", course_recommendation, name="course recommendation"),
    path("combination/", uace_combination, name="uace recommendation"),
    path("uace_subjects/", uace_subjects, name="uace"),
    path("uce_subjects/", uce_subjects, name="uce"),
]



#     path("careers/", CareersClass.as_view(), name="CareersClass"),
# path("signup/", signup, name="signup"),
# path("testing/", testing, name="testing"),