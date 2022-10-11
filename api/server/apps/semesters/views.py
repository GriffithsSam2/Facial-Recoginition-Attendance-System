from urllib import request
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.semesters.logic.serializers import SemesterSerializer
from server.apps.semesters.models import Semester
from server.settings.components import pagination


class SemesterViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all().order_by('-semester_year', '-semester')
    pagination_class = pagination.StandardResultsSetPagination


class SearchSemesterAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all().order_by('-semester_year', '-semester')
    pagination_class = pagination.StandardResultsSetPagination

    def get_queryset(self):
        q__1 = self.kwargs['semester_year']
        q__2 = self.kwargs['other']

        qs = self.queryset.filter(semester_year=q__1, programme=q__2)

        if qs:
            return qs
        
        qs = self.queryset.filter(semester_year=q__1, department=q__2)
        return qs
