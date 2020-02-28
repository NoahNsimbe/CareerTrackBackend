from django.urls import path
from .views import get_uace_subjects, get_uce_subjects

urlpatterns = [

    path("uace_subjects/", get_uace_subjects, name="uace_list"),
    path("uce_subjects/", get_uce_subjects, name="uce_list"),
]