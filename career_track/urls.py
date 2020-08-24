from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenVerifyView
)
from main_app.api import UaceViewSet, CareersViewSet, UceViewSet, UaceCombinationViewSet, CourseRecommendationViewSet

admin.AdminSite.name = 'Course Recommendation'
admin.AdminSite.site_header = 'Course Recommendation'
admin.AdminSite.index_title = 'Course Recommendation'
admin.AdminSite.site_title = 'Course Recommendation'

router = routers.DefaultRouter()
router.register('uace_subjects', UaceViewSet)
router.register('uce_subjects', UceViewSet)
router.register('careers', CareersViewSet)
router.register('get_combination', UaceCombinationViewSet, basename="get_combination")
router.register('get_course', CourseRecommendationViewSet, basename="get_course")


urlpatterns = [

    path('api/admin/', admin.site.urls),
    path('admin/login/', auth_views.LoginView.as_view(), name='admin_login'),
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('openapi/', get_schema_view(
        title="Professers landing api",
        description="API for Professers landing site",
        version="v1"
    ), name='openapi-schema'),
    path('api-doc/', TemplateView.as_view(
        template_name='api-doc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    path('', include(router.urls)),
]
