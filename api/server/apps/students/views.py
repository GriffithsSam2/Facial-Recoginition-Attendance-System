from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from server.apps.students.logic.serializers import StudentSerializer
from server.apps.students.models import Student
from server.settings.components import pagination


class StudentViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all().order_by('first_name', 'last_name')
    pagination_class = pagination.StandardResultsSetPagination


class AllStudentsAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    
class SearchStudentsAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    pagination_class = pagination.StandardResultsSetPagination

    def get_queryset(self):
        q__1 = self.kwargs['first_name']
        q__2 = self.kwargs['last_name']
        q__3 = self.kwargs['programme']

        return self.queryset.filter(first_name=q__1, last_name=q__2, programme=q__3)
