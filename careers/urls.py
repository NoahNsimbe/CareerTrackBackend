from django.urls import path
from .views import get_careers, CareersClass

urlpatterns = [
    # path("careers/", get_careers, name="careers_list"),
    path("careers/", CareersClass.as_view(), name="CareersClass"),
]