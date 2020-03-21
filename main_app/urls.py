from django.urls import path
from .views import signup, testing

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("testing/", testing, name="testing")
]