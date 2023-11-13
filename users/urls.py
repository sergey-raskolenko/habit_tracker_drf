from django.urls import path

from users.apps import UsersConfig

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from users.views import UserListView, UserRegistrationAPIView, UserReadUpdateDeleteView

app_name = UsersConfig.name


urlpatterns = [
	path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('users/', UserListView.as_view(), name='list_user'),
	path('users/<int:pk>/', UserReadUpdateDeleteView.as_view(), name='update_user'),
	path('register/', UserRegistrationAPIView.as_view(), name='register_user'),
]
