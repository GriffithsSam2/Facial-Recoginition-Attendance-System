from rest_framework import serializers

from server.apps.attendances.models import TempPhoto, StudentAttendance, LecturerAttendance


class AttendanceRecordSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = TempPhoto
        fields = '__all__'


class AttendanceSerializer(serializers.Serializer):    
    pass
