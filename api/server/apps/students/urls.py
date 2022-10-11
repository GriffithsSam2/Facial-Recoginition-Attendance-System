from django.urls import path

from rest_framework.routers import DefaultRouter

from server.apps.students.views import StudentViewSet, SearchStudentsAPIView, AllStudentsAPIView


app_name = 'students'
router = DefaultRouter()
router.register(r'', StudentViewSet, basename='students')
urlpatterns = [
    path('all/', AllStudentsAPIView.as_view(), name='all_students'),
    path('search/<str:first_name>/<str:last_name>/<str:programme>/', SearchStudentsAPIView.as_view(), name='search_student'),
]
urlpatterns += router.urls
