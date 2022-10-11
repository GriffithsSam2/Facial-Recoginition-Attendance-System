from rest_framework import serializers

from server.apps.students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'dob', 'programme', 'student_id', 'entry_date', 'photo')
