from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UserRegisterSerializer, UserSerializer


class UserRegistrationAPIView(CreateAPIView):
	queryset = User.objects.all()
	permission_classes = [AllowAny]
	serializer_class = UserRegisterSerializer


class UserListView(ListAPIView):
	queryset = User.objects.all()
	permission_classes = [AllowAny]
	serializer_class = UserSerializer


class UserUpdateView(RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	permission_classes = [IsCurrentUser]
	serializer_class = UserSerializer
