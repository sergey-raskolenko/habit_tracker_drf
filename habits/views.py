from rest_framework import generics, serializers
from rest_framework.response import Response

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitPublicListSerializer, HabitSerializer


class HabitListView(generics.ListAPIView):
	serializer_class = HabitSerializer
	pagination_class = HabitPaginator

	def get_queryset(self):
		return Habit.objects.filter(owner=self.request.user)


class PublicHabitListView(generics.ListAPIView):
	serializer_class = HabitPublicListSerializer
	pagination_class = HabitPaginator

	def get_queryset(self):
		return Habit.objects.filter(is_public=True)


class HabitCreateView(generics.CreateAPIView):
	serializer_class = HabitSerializer

	def perform_create(self, serializer):
		new_habit = serializer.save()
		new_habit.owner = self.request.user
		new_habit.save()


class HabitReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = HabitSerializer
	queryset = Habit.objects.all()
	permission_classes = [IsOwner]
