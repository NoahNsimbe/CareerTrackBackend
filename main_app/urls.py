from django.urls import path
from .views import signup, testing, course_recommendation, CareersClass, uace_combination

urlpatterns = [
    path("signup/", signup, name="signup"),
# path("careers/", get_careers, name="careers_list"),
    path("careers/", CareersClass.as_view(), name="CareersClass"),
    path("testing/", testing, name="testing"),
    path("course_recommendation/", course_recommendation, name="course recommendation"),
    path("uace_combination/", uace_combination, name="uace recommendation")
]