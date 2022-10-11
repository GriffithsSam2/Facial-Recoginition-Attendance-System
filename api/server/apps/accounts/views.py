from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from server.apps.accounts.models import User
from server.apps.accounts.logic.serializers import PasswordSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from server.settings.components import pagination


class RegisterAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        return Response(
            data={
                'code': status.HTTP_200_OK,
                'data': data
            },
            status=status.HTTP_200_OK
        )


class UserListAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('first_name', 'last_name')
    pagination_class = pagination.StandardResultsSetPagination


class RetrieveUpdateDestroyUserAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class UpdatePasswordAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordSerializer
    queryset = User.objects.all()
    
    def patch(self, request, id):
        password = request.data['password']
        user: User = self.queryset.filter(id=id).first()

        if user:
            user.set_password(password)
            user.save()

            return Response({'message: Password successfully changed.'}, status.HTTP_200_OK)
        
        return Response({}, status.HTTP_404_NOT_FOUND)


class SearchUsersAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = pagination.StandardResultsSetPagination

    def get_queryset(self):
        q__1 = self.kwargs['first_name']
        q__2 = self.kwargs['last_name']

        return self.queryset.filter(first_name=q__1, last_name=q__2)
