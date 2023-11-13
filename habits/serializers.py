from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Habit
		fields = '__all__'
		read_only_fields = ('owner',)


class HabitPublicListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Habit
		exclude = ('is_public',)
