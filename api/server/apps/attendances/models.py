from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.students.models import Student
from server.apps.lecturers.models import Lecturer
from server.apps.semesters.models import Semester


def temp_image_file(instance, filename):
    return '/'.join(['images', 'temp', '', filename])

    
class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    attendance = models.IntegerField(_('Attendance'), default=0)


class LecturerAttendance(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    attendance = models.IntegerField(_('Attendance'), default=0)


class TempPhoto(models.Model):
    photo = models.ImageField(_('Photo'), upload_to=temp_image_file)
