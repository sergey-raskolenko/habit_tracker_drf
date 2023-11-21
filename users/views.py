from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UserRegisterSerializer, UserSerializer


class UserRegistrationAPIView(CreateAPIView):
	"""Контроллер для регистрации пользователя"""
	queryset = User.objects.all()
	permission_classes = [AllowAny]
	serializer_class = UserRegisterSerializer


class UserListView(ListAPIView):
	"""Контроллер для отображения списка пользователей"""
	queryset = User.objects.all()
	permission_classes = [AllowAny]
	serializer_class = UserSerializer


class UserReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
	"""Контроллер для детального просмотра, изменения и удаления пользователя. Доступен для владельца пользователя"""
	queryset = User.objects.all()
	permission_classes = [IsCurrentUser]
	serializer_class = UserSerializer
