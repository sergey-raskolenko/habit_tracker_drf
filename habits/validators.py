from rest_framework import serializers


class TimeForActionValidator:
	"""Валидатор на основе класса для проверки времени выполнения"""
	def __init__(self, field):
		self.field = field

	def __call__(self, value):
		tmp_value = dict(value).get(self.field)
		if tmp_value and not 0 < tmp_value <= 120:
			raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд.')
