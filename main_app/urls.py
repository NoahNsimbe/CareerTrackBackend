from django.urls import path
from .views import course_recommendation, uace_combination, get_careers

urlpatterns = [
    path("careers/", get_careers, name="careers_list"),
    path("course_recommendation/", course_recommendation, name="course recommendation"),
    path("combination/", uace_combination, name="uace recommendation")
]



#     path("careers/", CareersClass.as_view(), name="CareersClass"),
# path("signup/", signup, name="signup"),
# path("testing/", testing, name="testing"),