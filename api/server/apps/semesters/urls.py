from django.urls import path

from rest_framework.routers import DefaultRouter

from server.apps.semesters.views import SemesterViewSet, SearchSemesterAPIView


app_name = 'semesters'
router = DefaultRouter()
router.register(r'', SemesterViewSet, basename='semesters')
urlpatterns = [
    path('search/<str:semester_year>/<str:other>/', SearchSemesterAPIView.as_view(), name='search_semester'),
]
urlpatterns += router.urls
