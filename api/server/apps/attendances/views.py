from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import permissions, status
from rest_framework.response import Response

from server.apps.attendances.logic.serializers import AttendanceRecordSerializer, AttendanceSerializer
from server.apps.attendances.logic.utils import Attendance
from server.apps.attendances.models import StudentAttendance, LecturerAttendance, TempPhoto
from server.apps.lecturers.models import Lecturer
from server.apps.semesters.models import Semester
from server.apps.students.models import Student


class RecordStudentAttendanceAPIView(GenericAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, student_id):
        student = Student.objects.filter(id=student_id).first()
        if student:
            semester = Semester.objects.filter(programme=student.programme, is_current=True).first()

            if semester:
                attendance: StudentAttendance = StudentAttendance.objects.filter(student=student, semester=semester).first()
                            
                if attendance:
                    attendance.attendance += 1
                    attendance.save()
                else:
                    StudentAttendance.objects.create(student=student, semester=semester, attendance=1)

                return Response({'message': 'Successfully recorded.'}, status.HTTP_200_OK)

        return Response({'message': 'Failed.'}, status.HTTP_404_NOT_FOUND)


class RecordLectureAttendanceAPIView(GenericAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, student_id):
        lecturer = Lecturer.objects.filter(id=student_id).first()

        if lecturer:
            semester = Semester.objects.filter(department=lecturer.department, is_current=True).first()

            if semester:
                attendance: LecturerAttendance = LecturerAttendance.objects.filter(lecturer=lecturer, semester=semester).first()
                            
                if attendance:
                    attendance.attendance += 1
                    attendance.save()
                else:
                    LecturerAttendance.objects.create(lecturer=lecturer, semester=semester, attendance=1)

                return Response({'message': 'Successfully recorded.'}, status.HTTP_200_OK)

        return Response({'message': 'Failed.'}, status.HTTP_404_NOT_FOUND)


class RetrieveStudentAttendanceRecordAPIView(GenericAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = StudentAttendance.objects.all()

    def get(self, request, student_id):
        data = Attendance.retrieve_student_attendance(student_id)
        status_code = status.HTTP_200_OK if data else status.HTTP_404_NOT_FOUND
        return Response(data, status=status_code)


class RetrieveLecturerAttendanceRecordAPIView(GenericAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = LecturerAttendance.objects.all()

    def get(self, request, lecturer_id):
        data = Attendance.retrieve_lecturer_attendance(lecturer_id)
        status_code = status.HTTP_200_OK if data else status.HTTP_404_NOT_FOUND
        return Response(data, status=status_code)
