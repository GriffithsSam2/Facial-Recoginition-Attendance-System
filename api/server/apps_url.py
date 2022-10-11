from django.urls import include, path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from server.apps.accounts import urls as account_urls
from server.apps.semesters import urls as semester_urls
from server.apps.lecturers import urls as lecturer_urls
from server.apps.students import urls as student_urls
from server.apps.attendances import urls as attendance_urls


schema_view = get_schema_view(
   openapi.Info(
      title="Attendance API",
      default_version='v1',
      description="Enpoints for developing attendance application softwares.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('api/accounts/', include(account_urls, namespace='accounts')),
    path('api/semesters/', include(semester_urls, namespace='semesters')),
    path('api/lecturers/', include(lecturer_urls, namespace='lecturers')),
    path('api/students/', include(student_urls, namespace='students')),
	path('api/attendances/', include(attendance_urls, namespace='attendances')),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/download/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
