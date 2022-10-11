from rest_framework import serializers

from server.apps.lecturers.models import Lecturer


class LecturerSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = Lecturer
        fields = ('id', 'first_name', 'last_name', 'dob', 'department', 'photo')
