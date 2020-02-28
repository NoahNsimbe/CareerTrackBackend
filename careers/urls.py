from django.urls import path
from .views import get_careers

urlpatterns = [
    path("careers/", get_careers, name="careers_list"),
]