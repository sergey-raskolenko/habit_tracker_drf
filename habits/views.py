from rest_framework import generics, serializers
from rest_framework.response import Response

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitPublicListSerializer, HabitSerializer
from habits.services import send_welcome_message, create_periodic_task


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
		if not new_habit.is_enjoyable:
			send_welcome_message(new_habit)
			create_periodic_task(new_habit)


class HabitReadUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = HabitSerializer
	queryset = Habit.objects.all()
	permission_classes = [IsOwner]
