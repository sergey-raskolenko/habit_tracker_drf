from rest_framework import serializers

from habits.models import Habit
from habits.validators import TimeForActionValidator


class HabitSerializer(serializers.ModelSerializer):
	"""Базовый сериализатор для объекта модели Habit"""

	def validate_linked_habit(self, value: Habit):
		"""Валидация для поля связанной привычки"""
		if value and not value.is_enjoyable:
			raise serializers.ValidationError(
				'В связанные привычки могут попадать только привычки с признаком приятной привычки.'
			)
		return value

	def validate(self, data):
		"""Общая валидация для исключения:
		1) одновременного указания связанной привычки и награды
		2) указания связанной привычки или награды у приятной привычки
		"""
		if data.get('linked_habit') and data.get('reward'):
			raise serializers.ValidationError(
				"Одновременный выбор связанной привычки и указание вознаграждения исключен."
			)
		if data.get('is_enjoyable') and (data.get('reward') or data.get('linked_habit')):
			raise serializers.ValidationError(
				"У приятной привычки не может быть вознаграждения или связанной привычки."
			)
		return data

	def update(self, instance, validated_data):
		"""Валидация при обновлении при:
		1) присвоения награды/связанной привычки при существующей связанной привычке/награде
		2) указания связанной привычки или награды у приятной привычки
		"""
		if instance.reward and validated_data.get("linked_habit") is not None \
			or instance.linked_habit and validated_data.get('reward') is not None:
			raise serializers.ValidationError(
				"Одновременный выбор связанной привычки и указание вознаграждения исключен."
			)
		if instance.is_enjoyable and \
			(validated_data.get("linked_habit") is not None or validated_data.get('reward') is not None):
			raise serializers.ValidationError(
				"У приятной привычки не может быть вознаграждения или связанной привычки."
			)
		return super().update(instance, validated_data)

	class Meta:
		model = Habit
		fields = '__all__'
		read_only_fields = ('owner',)
		validators = [TimeForActionValidator(field='time_for_action')]


class HabitPublicListSerializer(serializers.ModelSerializer):
	"""Сериализатор для публичного представления привычки"""

	class Meta:
		model = Habit
		exclude = ('is_public',)
