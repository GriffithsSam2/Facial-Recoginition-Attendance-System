from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from server.apps.attendances import views


app_name = 'accounts'

urlpatterns = [
    path('record/student/<int:student_id>/', views.RecordStudentAttendanceAPIView.as_view(), name='record-attendance-student'),
    path('record/lecturer/<int:lecturer_id>/', views.RecordLectureAttendanceAPIView.as_view(), name='record-attendance-lecturer'),
    path('retrieve/student/<int:student_id>/', views.RetrieveStudentAttendanceRecordAPIView.as_view(), name='retrieve-attendance-student'),
    path('retrieve/lecturer/<int:lecturer_id>/', views.RetrieveLecturerAttendanceRecordAPIView.as_view(), name='retrieve-attendance-lecturer'),
]
