from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from server.apps.lecturers.logic.serializers import LecturerSerializer
from server.apps.lecturers.models import Lecturer
from server.settings.components import pagination


class LecturerViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.all().order_by('first_name', 'last_name')
    pagination_class = pagination.StandardResultsSetPagination


class AllLecturersAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.all().order_by('first_name', 'last_name')


class SearchLecturersAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.all()
    pagination_class = pagination.StandardResultsSetPagination

    def get_queryset(self):
        q__1 = self.kwargs['first_name']
        q__2 = self.kwargs['last_name']
        q__3 = self.kwargs['department']

        return self.queryset.filter(first_name=q__1, last_name=q__2, department=q__3)
