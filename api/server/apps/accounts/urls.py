from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from server.apps.accounts import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('users/', views.UserListAPIView.as_view(), name='users'),
    path('search/<str:first_name>/<str:last_name>/', views.SearchUsersAPIView.as_view(), name='search_user'),
    path('update/password/<int:id>/', views.UpdatePasswordAPIView.as_view(), name='update_password'),
    path('users/<int:id>/', views.RetrieveUpdateDestroyUserAPIView.as_view(), name='user_update'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
