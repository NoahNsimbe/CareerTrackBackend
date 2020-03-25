from django.urls import path
from .views import signup, testing, course_without_results, CareersClass, course_with_results

urlpatterns = [
    path("signup/", signup, name="signup"),
# path("careers/", get_careers, name="careers_list"),
    path("careers/", CareersClass.as_view(), name="CareersClass"),
    path("testing/", testing, name="testing"),
    path("course_without_results/", course_without_results, name="course recommendation without results"),
    path("course_with_results/", course_with_results, name="course recommendation with results")
]