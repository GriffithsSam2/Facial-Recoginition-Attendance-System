from django.urls import path

from rest_framework.routers import DefaultRouter

from server.apps.lecturers.views import LecturerViewSet, SearchLecturersAPIView, AllLecturersAPIView


app_name = 'lecturers'
router = DefaultRouter()
router.register(r'', LecturerViewSet, basename='lecturers')
urlpatterns = [
    path('all/', AllLecturersAPIView.as_view(), name='all_lecturers'),
    path('search/<str:first_name>/<str:last_name>/<str:department>/', SearchLecturersAPIView.as_view(), name='search_lecturer'),
]
urlpatterns += router.urls
