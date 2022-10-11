from rest_framework import serializers
from server.apps.semesters.models import Semester


class SemesterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    department = serializers.CharField(required=False)
    programme = serializers.CharField(required=False)
    is_current = serializers.BooleanField(default=False)

    class Meta:
        model = Semester
        fields = ('id', 'member', 'department', 'programme', 'semester_year', 'semester', 'attendance', 'is_current')
