
from django.db.models import QuerySet

from server.apps.semesters.models import Semester
from server.apps.students.models import Student
from server.apps.lecturers.models import Lecturer
from server.apps.attendances.models import StudentAttendance, LecturerAttendance


class Attendance:
    @staticmethod
    def retrieve_student_attendance(student_id):
        student: Student = Student.objects.filter(id=student_id).first()
        
        if student:
            semester: Semester = Semester.objects.filter(programme=student.programme, is_current=True).first()

            if semester:
                attendance: StudentAttendance = StudentAttendance.objects.filter(student=student, semester=semester).first()

                if attendance:
                    attendance = attendance.attendance
                else:
                    attendance = 0

                return  {
                    'student_id': student.id,
                    'attendance': attendance,
                    'semester': semester.semester,
                    'semester_year': semester.semester_year,
                }

        return {}

    @staticmethod
    def retrieve_lecturer_attendance(lecturer_id):
        lecturer: Lecturer = Lecturer.objects.filter(id=lecturer_id).first()
        
        if lecturer:
            semester: Semester = Semester.objects.filter(department=lecturer.department, is_current=True).first()

            if semester:
                attendance: LecturerAttendance = LecturerAttendance.objects.filter(lecturer=lecturer, semester=semester).first()

                if attendance:
                    attendance = attendance.attendance
                else:
                    attendance = 0

                return  {
                    'lecturer_id': lecturer.id,
                    'attendance': attendance,
                    'semester': semester.semester,
                    'semester_year': semester.semester_year,
                }

        return {}
